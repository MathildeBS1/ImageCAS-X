"""Explore and quality-check the Medis-derived coronary centerlines (Herlev-Østerbro / CGPS
baseline cohort, 744 cases) that Kit uploaded to /data/kimbr/centerlines_hø_10Y.zip.

    python centerline_qc.py                                # uses ZIP_PATH and OUT_DIR below
    python centerline_qc.py --src /path/to/zip_or_folder --out ~/centerline_qc
    python centerline_qc.py --inspect                      # only list what is in the zip
    python centerline_qc.py --limit 20                     # quick trial on the first 20 cases

Needs numpy, pandas and matplotlib (all in the base conda env). scipy is used if present (faster
nearest-neighbour search). Legacy .vtk files (Kit's <id>_centerline.vtk; ASCII or binary, VTK 4.x or
5.1) are read without extra packages; only binary/compressed .vtp needs `pip install vtk`.
Files that are not centerlines (e.g. analysis_processed.log) are not counted as cases; the start
of the log is shown in inventory.md.

The zip is read in place (nothing is extracted, the zip is never modified). Everything is written
to OUT_DIR:
- inventory.md        what is in the zip: file types, folder layout, guessed cases, the first lines
                      / data arrays of one example file per type. Start here: if the parser did
                      not understand the files, this shows why (and what to change).
- report.md           the quality report: segment presence, lengths per segment, unlabelled
                      length, branch points, connected components, expected segment
                      connections (LM->LAD/LCX, LAD->D1, ...), unexpected contacts, red flags.
- per_case.csv        one row per case with all per-case metrics and flags.
- segment_lengths.csv one row per case x segment (length in mm).
- label_values.csv    every raw label value seen and how it was mapped to a segment name.
- figures/*.png       length distributions per segment, unlabelled %, branch points, presence.
The report and CSVs contain case IDs (file / folder names); keep them on the DTU machine.

How the checks work
- Every file is turned into polylines (ordered 3D points in mm) with a segment label per point.
  Labels come from a point/cell array or JSON/CSV field whose name looks like a label
  (label, segment, class, name, vessel, ...), or from the JSON key / file name they sit under.
- Polylines are joined into one graph per case: points closer than DEDUP_TOL are the same node,
  and a polyline end is joined to the nearest point of another polyline if it is within
  JOIN_TOL mm. Branch points = nodes with >= 3 neighbours, end points = 1 neighbour.
- Lengths are summed over unique graph edges, so overlapping polylines (e.g. every branch
  exported from the ostium) are not double counted; the overlap itself is reported.
- Two segments are "connected" if a graph edge joins them directly, or "via unlabelled" if they
  both touch the same stretch of unlabelled points.
Raw labels are mapped to SCCT-style names (LM, pLAD, mLAD, dLAD, D1, D2, IM, pCX, mCX, dCX, OM1,
OM2, pRCA, mRCA, dRCA, PDA, PLA) by normalise_label(); check label_values.csv that the mapping is
right. Numeric labels 1-18 are read as the SCCT 18-segment numbers when LABEL_NUMBERING = "auto"
and every numeric label is in 0-18 (0 = unlabelled) - confirm this with Kit.
"""

from __future__ import annotations

import argparse
import fnmatch
import io
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# ---- edit these before running (or override with --src / --out) ----
ZIP_PATH = "/data/kimbr/centerlines_hø_10Y.zip"   # the zip, or a folder with the extracted files
OUT_DIR = str(Path.home() / "centerline_qc")       # results folder (created if missing)

EXPECTED_CASES = 744
DEDUP_TOL = 0.01      # mm: points closer than this are the same graph node
JOIN_TOL = 1.0        # mm: a polyline end this close to another polyline is joined to it
GAP_FACTOR = 5.0      # a step > GAP_FACTOR x median spacing (and > GAP_MIN mm) is a gap
GAP_MIN = 3.0         # mm
OVERLAP_TOL = 0.5     # mm: a point this close to another polyline (not at its ends) overlaps it
SHORT_SEGMENT = 2.0   # mm: labelled segments shorter than this are flagged
LABEL_NUMBERING = "auto"   # "auto", "scct" (numbers are SCCT 18-segment codes) or "raw"
CODE_NAMES = {}       # names for label codes no file names, once Kit confirms them, e.g. {18: "D3", 22: "OM2"}
COMPLETE_RCA_NEEDS_DRCA = True  # complete_trunks: LAD, CX and RCA trunks all complete; False = RCA only needs pRCA + mRCA
CASE_FROM = "auto"    # "auto", "folder" (first folder under the common root = case) or "file"
SKIP = ("__MACOSX/*", "*/.DS_Store", ".DS_Store", "*/._*", "._*", "*/Thumbs.db")

TEXT_EXT = {".json", ".csv", ".txt", ".tsv", ".dat", ".xml", ".vtk", ".vtp", ".ctl", ".cl"}
PARSEABLE = {".json", ".csv", ".txt", ".tsv", ".dat", ".xml", ".vtk", ".vtp", ".npy", ".npz",
             ".ctl", ".cl"}
LABEL_HINTS = ("label", "segment", "seg", "class", "name", "vessel", "artery", "branch", "type",
               "tag", "id")
RADIUS_HINTS = ("radius", "maximuminscribed", "diameter")
GENERIC_KEYS = {"points", "point", "centerline", "centerlines", "centreline", "coordinates",
                "coords", "data", "path", "paths", "vertices", "nodes", "positions", "xyz",
                "branches", "segments", "lines", "items", "values", "polyline", "polylines"}

# ---- segment names ----
SEGMENTS = ("LM", "pLAD", "mLAD", "dLAD", "LAD", "D1", "D2", "D3", "IM",
            "pCX", "mCX", "dCX", "CX", "OM1", "OM2", "OM3",
            "pRCA", "mRCA", "dRCA", "RCA", "PDA", "PLA")
LAD = {"pLAD", "mLAD", "dLAD", "LAD"}
CX = {"pCX", "mCX", "dCX", "CX"}
RCA = {"pRCA", "mRCA", "dRCA", "RCA"}
SCCT = {1: "pRCA", 2: "mRCA", 3: "dRCA", 4: "PDA", 5: "LM", 6: "pLAD", 7: "mLAD", 8: "dLAD",
        9: "D1", 10: "D2", 11: "pCX", 12: "OM1", 13: "mCX", 14: "OM2", 15: "PDA", 16: "PLA",
        17: "IM", 18: "PLA"}
ALIASES = {
    "lm": "LM", "lmca": "LM", "leftmain": "LM", "lmain": "LM", "mainstem": "LM", "lms": "LM",
    "plad": "pLAD", "ladp": "pLAD", "proximallad": "pLAD", "ladproximal": "pLAD", "lad1": "pLAD",
    "mlad": "mLAD", "ladm": "mLAD", "midlad": "mLAD", "ladmid": "mLAD", "lad2": "mLAD",
    "dlad": "dLAD", "ladd": "dLAD", "distallad": "dLAD", "laddistal": "dLAD", "lad3": "dLAD",
    "lad": "LAD", "leftanteriordescending": "LAD",
    "d1": "D1", "diag1": "D1", "diagonal1": "D1", "firstdiagonal": "D1",
    "d2": "D2", "diag2": "D2", "diagonal2": "D2", "seconddiagonal": "D2",
    "d3": "D3", "diag3": "D3", "diagonal3": "D3",
    "im": "IM", "ri": "IM", "ramus": "IM", "ramusintermedius": "IM", "intermediate": "IM",
    "pcx": "pCX", "plcx": "pCX", "pcfx": "pCX", "cxp": "pCX", "lcxp": "pCX", "proximalcx": "pCX",
    "proximallcx": "pCX", "lcx1": "pCX", "cx1": "pCX",
    "mcx": "mCX", "mlcx": "mCX", "cxm": "mCX", "lcxm": "mCX", "midcx": "mCX", "midlcx": "mCX",
    "lcx2": "mCX", "cx2": "mCX",
    "dcx": "dCX", "dlcx": "dCX", "cxd": "dCX", "lcxd": "dCX", "distalcx": "dCX",
    "distallcx": "dCX", "lcx3": "dCX", "cx3": "dCX",
    "cx": "CX", "lcx": "CX", "circumflex": "CX", "leftcircumflex": "CX",
    "om1": "OM1", "om2": "OM2", "om3": "OM3", "om": "OM1",
    "prca": "pRCA", "rcap": "pRCA", "proximalrca": "pRCA", "rca1": "pRCA",
    "mrca": "mRCA", "rcam": "mRCA", "midrca": "mRCA", "rca2": "mRCA",
    "drca": "dRCA", "rcad": "dRCA", "distalrca": "dRCA", "rca3": "dRCA",
    "rca": "RCA", "rightcoronary": "RCA", "rightcoronaryartery": "RCA",
    "pda": "PDA", "rpda": "PDA", "lpda": "PDA", "posteriordescending": "PDA",
    "pla": "PLA", "plb": "PLA", "rplb": "PLA", "lplb": "PLA", "pl": "PLA", "rpl": "PLA",
    "lpl": "PLA", "posterolateral": "PLA",
}
UNLABELLED = {"", "none", "nan", "null", "unknown", "unlabeled", "unlabelled", "other", "0", "-1",
              "background", "undefined", "na", "n/a"}
# (child, allowed parents): the child should touch at least one of them
EXPECTED = [
    ("pLAD", {"LM"}), ("pCX", {"LM"}), ("mLAD", {"pLAD"}), ("dLAD", {"mLAD"}),
    ("mCX", {"pCX"}), ("dCX", {"mCX"}), ("mRCA", {"pRCA"}), ("dRCA", {"mRCA"}),
    ("LAD", {"LM", "pLAD"}), ("CX", {"LM", "pCX"}),  # unsplit trunk, e.g. Kit's "13:LCx" after pCx
    ("D1", LAD), ("D2", LAD), ("D3", LAD), ("IM", {"LM", "pLAD", "pCX", "LAD", "CX"}),
    ("OM1", CX), ("OM2", CX), ("OM3", CX),
    ("PDA", RCA | CX), ("PLA", RCA | CX | {"PDA"}),
]
EXPECTED_PAIRS = {frozenset((c, p)) for c, ps in EXPECTED for p in ps}
# contacts that should never happen (whole-artery level)
TERRITORY = {**{s: "LM" for s in ("LM",)}, **{s: "LAD" for s in LAD | {"D1", "D2", "D3"}},
             **{s: "CX" for s in CX | {"OM1", "OM2", "OM3"}}, **{s: "RCA" for s in RCA},
             "IM": "IM", "PDA": "PDA", "PLA": "PLA"}
IMPOSSIBLE = {frozenset(p) for p in (("LAD", "RCA"), ("LM", "RCA"), ("CX", "RCA"))}


# ============================================================ reading the source
class Source:
    """A zip (read in place, nested zips included) or a folder; members are relative paths."""

    def __init__(self, path):
        self.path = Path(path).expanduser()
        self.nested = {}
        if self.path.is_dir():
            self.zip = None
            self.members = sorted(str(p.relative_to(self.path)) for p in self.path.rglob("*")
                                  if p.is_file())
        else:
            self.zip = zipfile.ZipFile(self.path)
            self.members = []
            for info in self.zip.infolist():
                if info.is_dir():
                    continue
                if info.filename.lower().endswith(".zip"):
                    inner = zipfile.ZipFile(io.BytesIO(self.zip.read(info)))
                    for i in inner.infolist():
                        if not i.is_dir():
                            name = info.filename[:-4] + "/" + i.filename
                            self.nested[name] = (inner, i.filename)
                            self.members.append(name)
                else:
                    self.members.append(info.filename)
        self.members = [m for m in self.members if not any(fnmatch.fnmatch(m, p) for p in SKIP)]

    def read(self, name) -> bytes:
        if name in self.nested:
            z, inner = self.nested[name]
            return z.read(inner)
        if self.zip is None:
            return (self.path / name).read_bytes()
        return self.zip.read(name)


def ext(name):
    n = name.lower()
    for e in (".nii.gz", ".vtk.gz", ".json.gz", ".csv.gz"):
        if n.endswith(e):
            return e
    return Path(n).suffix


def group_cases(members):
    """{case_id: [member, ...]}: one folder per case, or one file per case. Files the script
    cannot read (e.g. a .log) are not cases; they are listed in the inventory only."""
    members = [m for m in members if ext(m) in PARSEABLE or ext(m).endswith(".gz")]
    parts = [m.split("/") for m in members]
    root = 0  # strip folders shared by every member
    while parts and all(len(p) > root + 1 for p in parts) and len({p[root] for p in parts}) == 1:
        root += 1
    mode = CASE_FROM
    if mode == "auto":
        mode = "folder" if all(len(p) > root + 1 for p in parts) else "file"
    cases = defaultdict(list)
    for m, p in zip(members, parts):
        if mode == "folder" and len(p) > root + 1:
            cid = p[root]
        else:
            cid = re.sub(r"(\.[A-Za-z0-9]+)+$", "", p[-1])
            cid = re.sub(r"[_\-\s]?(centerlines?|centrelines?|cl)$", "", cid, flags=re.I) or cid
        cases[cid].append(m)
    natural = lambda c: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", c[0])]
    return dict(sorted(cases.items(), key=natural)), mode, "/".join(parts[0][:root]) if parts else ""


# ============================================================ parsing into polylines
class Poly:
    def __init__(self, pts, labels=None, radius=None, source="", explicit=True):
        self.pts = np.asarray(pts, float).reshape(-1, 3)
        n = len(self.pts)
        self.labels = list(labels) if labels is not None else [None] * n
        self.radius = None if radius is None else np.asarray(radius, float).reshape(-1)
        self.source = source
        self.explicit = explicit  # connectivity given by the file (not inferred from row order)


NOT_LABELS = ("centerlineid", "groupid", "tractid", "blanking", "cellid", "pointid", "frenet",
              "abscissa", "curvature", "torsion", "normal", "tangent")


def label_like(name):
    n = name.lower()
    if any(x in n.replace("_", "") for x in NOT_LABELS):
        return False
    return any(h in n for h in LABEL_HINTS) and not any(h in n for h in RADIUS_HINTS)


def pick_label_array(arrays):
    """Choose the array that most looks like a segment label. arrays: {name: values}."""
    best, best_score = None, -1
    for name, v in arrays.items():
        if not label_like(name):
            continue
        v = np.asarray(v)
        if v.ndim > 1 and v.shape[1] != 1:
            continue
        n_unique = len(set(map(str, v.ravel()[:100000])))
        if n_unique > 64:
            continue
        n = name.lower()
        score = 3 if any(h in n for h in ("label", "segment", "class", "name", "vessel")) else 1
        if score > best_score:
            best, best_score = name, score
    return best


def pick_radius_array(arrays):
    for name, v in arrays.items():
        if any(h in name.lower() for h in RADIUS_HINTS) and np.asarray(v).ndim == 1:
            return name
    return None


def lookup_from_field(fd):
    """{code: "code:name"} from a string array like ["1:pRCA", "5:LM", ...] (Kit's segment_names)."""
    for v in fd.values():
        v = np.asarray(v, object).ravel()
        pairs = [re.match(r"^\s*(-?\d+)\s*:\s*(.+?)\s*$", str(x)) for x in v]
        if len(v) and all(pairs):
            return {int(m.group(1)): f"{m.group(1)}:{m.group(2)}" for m in pairs}
    return None


def coded_array(arrays, lookup):
    """A 1-component integer array whose values are (mostly) codes in the lookup."""
    for name, v in arrays.items():
        v = np.asarray(v)
        if v.dtype == object or v.ndim != 1 or not len(v) or not np.all(np.mod(v, 1) == 0):
            continue
        if np.isin(np.unique(v).astype(int), list(lookup)).mean() >= 0.8:
            return name
    return None


def polys_from_mesh(points, lines, point_arrays, cell_arrays, source, lookup=None):
    """Polylines from a VTK-style mesh: points (n,3), lines = list of index lists. lookup maps
    integer label codes to "code:name" strings."""
    lab_p = lab_c = None
    if lookup:
        lab_p = coded_array(point_arrays, lookup)
        lab_c = coded_array(cell_arrays, lookup) if lab_p is None else None
    if lab_p is None and lab_c is None:
        lab_p = pick_label_array(point_arrays)
        lab_c = pick_label_array(cell_arrays) if lab_p is None else None
    rad = pick_radius_array(point_arrays)
    if not lines:  # points only: treat as one ordered polyline
        lines = [list(range(len(points)))]
    out = []
    for ci, idx in enumerate(lines):
        if len(idx) < 2:
            continue
        idx = np.asarray(idx, int)
        if lab_p is not None:
            labels = [_scalar(point_arrays[lab_p][i]) for i in idx]
        elif lab_c is not None and ci < len(cell_arrays[lab_c]):
            labels = [_scalar(cell_arrays[lab_c][ci])] * len(idx)
        else:
            labels = None
        if lookup and labels is not None:
            labels = [lookup.get(int(l), l) if isinstance(l, (int, float, np.number)) and l == l else l
                      for l in labels]
        r = np.asarray(point_arrays[rad])[idx] if rad else None
        out.append(Poly(np.asarray(points)[idx], labels, r, source))
    meta = {"point_arrays": list(point_arrays), "cell_arrays": list(cell_arrays),
            "label_array": lab_p or lab_c, "label_lookup": bool(lookup), "n_lines": len(lines)}
    return out, meta


def _scalar(v):
    v = np.asarray(v).ravel()
    return v[0].item() if v.size and hasattr(v[0], "item") else (v[0] if v.size else None)


def parse_vtk_lib(data, e):
    try:
        import vtk
        from vtk.util.numpy_support import vtk_to_numpy
    except ImportError:
        return None
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=e) as f:
        f.write(data)
        f.flush()
        r = vtk.vtkXMLPolyDataReader() if e == ".vtp" else vtk.vtkPolyDataReader()
        r.SetFileName(f.name)
        r.ReadAllScalarsOn() if hasattr(r, "ReadAllScalarsOn") else None
        r.ReadAllFieldsOn() if hasattr(r, "ReadAllFieldsOn") else None
        r.Update()
        pd_ = r.GetOutput()
    if pd_ is None or pd_.GetNumberOfPoints() == 0:
        return [], {"error": "vtk read no points"}
    pts = vtk_to_numpy(pd_.GetPoints().GetData())
    lines, ids = [], vtk.vtkIdList()
    ca = pd_.GetLines()
    ca.InitTraversal()
    while ca.GetNextCell(ids):
        lines.append([ids.GetId(i) for i in range(ids.GetNumberOfIds())])

    def arrays(attr):
        out = {}
        for i in range(attr.GetNumberOfArrays()):
            a = attr.GetAbstractArray(i)
            if a is None:
                continue
            if isinstance(a, vtk.vtkStringArray):
                out[a.GetName() or f"array{i}"] = np.array([a.GetValue(j) for j in range(a.GetNumberOfValues())], object)
            else:
                out[a.GetName() or f"array{i}"] = vtk_to_numpy(a)
        return out

    return polys_from_mesh(pts, lines, arrays(pd_.GetPointData()), arrays(pd_.GetCellData()), e)


VTK_DTYPES = {"unsigned_char": "u1", "char": "i1", "unsigned_short": "u2", "short": "i2",
              "unsigned_int": "u4", "int": "i4", "unsigned_long": "u8", "long": "i8", "float": "f4",
              "double": "f8", "vtktypeint64": "i8", "vtktypeuint64": "u8", "vtkidtype": "i8",
              "vtktypeint32": "i4", "vtktypeuint32": "u4"}


class _VtkCursor:
    """Walks through a legacy .vtk file (bytes): keyword lines, then ASCII or big-endian binary data."""

    def __init__(self, data):
        self.d, self.pos = data, 0

    def raw_line(self):
        j = self.d.find(b"\n", self.pos)
        j = len(self.d) if j < 0 else j
        s = self.d[self.pos:j].decode("latin-1").strip()
        self.pos = j + 1
        return s

    def line(self):
        """Next non-empty line, or None at the end of the file."""
        while self.pos < len(self.d):
            s = self.raw_line()
            if s:
                return s
        return None

    def peek(self):
        pos = self.pos
        s = self.line()
        self.pos = pos
        return s

    def skip_metadata(self):  # a METADATA block ends at the first empty line
        while self.pos < len(self.d) and self.raw_line():
            pass

    def values(self, n, dtype, binary):
        dtype = dtype.lower()
        if dtype == "string":
            if not binary:
                return np.array([self.line() for _ in range(n)], object)
            out = []
            for _ in range(n):  # top 2 bits of the first byte: 3 -> 1-byte, 2 -> 2, 1 -> 4, 0 -> 8-byte length
                kind = self.d[self.pos] >> 6
                size = {3: 1, 2: 2, 1: 4, 0: 8}[kind]
                length = int.from_bytes(self.d[self.pos:self.pos + size], "big") & ((1 << (8 * size - 2)) - 1)
                self.pos += size
                out.append(self.d[self.pos:self.pos + length].decode("utf-8", errors="replace"))
                self.pos += length
            return np.array(out, object)
        code = VTK_DTYPES.get(dtype)
        if code is None:
            raise ValueError(f"unknown VTK data type {dtype}")
        if binary:
            dt = np.dtype(">" + code)
            a = np.frombuffer(self.d, dt, n, self.pos).astype(dt.newbyteorder("="))
            self.pos += n * dt.itemsize
            return a
        out = []
        while len(out) < n:
            s = self.line()
            if s is None:
                raise ValueError("VTK file ended inside a data block")
            out += s.split()
        a = np.array(out[:n], float)
        return a if code[0] == "f" else a.astype(np.int64)


def parse_vtk_legacy(data):
    """Legacy .vtk POLYDATA, ASCII or BINARY, old (4.x) or new (5.1, OFFSETS/CONNECTIVITY) layout."""
    r = _VtkCursor(data)
    head = [r.raw_line() for _ in range(3)]  # version, title (may be empty), ASCII/BINARY
    if not head[0].lower().startswith("# vtk"):
        raise ValueError(f"not a legacy VTK file (first line {head[0][:40]!r})")
    binary = head[2].upper().startswith("BINARY")
    points, lines, pa, ca, fd = None, [], {}, {}, {}
    target, n_mode, keywords = fd, 0, Counter()
    while (s := r.line()) is not None:
        w = s.split()
        t = w[0].upper()
        keywords[t] += 1
        if t == "DATASET":
            if w[1].upper() != "POLYDATA":
                raise ValueError(f"DATASET {w[1]} (expected POLYDATA)")
        elif t == "POINTS":
            n = int(w[1])
            points = r.values(3 * n, w[2], binary).reshape(n, 3).astype(float)
        elif t in ("LINES", "VERTICES", "POLYGONS", "TRIANGLE_STRIPS"):
            n, size = int(w[1]), int(w[2])
            if (r.peek() or "").upper().startswith("OFFSETS"):  # VTK 5.1 layout
                offs = r.values(n, r.line().split()[1], binary).astype(int)
                conn = r.values(size, r.line().split()[1], binary).astype(int)
                cells = [list(conn[o0:o1]) for o0, o1 in zip(offs[:-1], offs[1:])]
            else:
                flat = r.values(size, "int", binary).astype(int)
                cells, j = [], 0
                while j < len(flat):
                    cells.append(list(flat[j + 1:j + 1 + flat[j]]))
                    j += flat[j] + 1
            if t == "LINES":
                lines += cells
        elif t in ("POINT_DATA", "CELL_DATA"):
            target, n_mode = (pa if t == "POINT_DATA" else ca), int(w[1])
        elif t == "SCALARS":
            ncomp = int(w[3]) if len(w) > 3 else 1
            if (r.peek() or "").upper().startswith("LOOKUP_TABLE"):
                r.line()
            target[w[1]] = r.values(n_mode * ncomp, w[2], binary).reshape(n_mode, ncomp).squeeze(1) \
                if ncomp == 1 else r.values(n_mode * ncomp, w[2], binary).reshape(n_mode, ncomp)
        elif t in ("VECTORS", "NORMALS"):
            target[w[1]] = r.values(3 * n_mode, w[2], binary).reshape(n_mode, 3)
        elif t == "TENSORS":
            target[w[1]] = r.values(9 * n_mode, w[2], binary).reshape(n_mode, 9)
        elif t == "TEXTURE_COORDINATES":
            target[w[1]] = r.values(int(w[2]) * n_mode, w[3], binary).reshape(n_mode, -1)
        elif t == "COLOR_SCALARS":
            r.values(int(w[2]) * n_mode, "unsigned_char" if binary else "float", binary)
        elif t == "LOOKUP_TABLE":
            r.values(4 * int(w[2]), "unsigned_char" if binary else "float", binary)
        elif t == "FIELD":
            for _ in range(int(w[2])):
                s = r.line()
                while s.upper().startswith("METADATA"):
                    r.skip_metadata()
                    s = r.line()
                name, ncomp, ntup, dt = s.split()[:4]
                arr = r.values(int(ncomp) * int(ntup), dt, binary)
                target[name] = arr.reshape(int(ntup), int(ncomp)) if int(ncomp) > 1 else arr
        elif t == "METADATA":
            r.skip_metadata()
        else:
            raise ValueError(f"unexpected line in VTK file: {s[:60]!r}")
    if points is None:
        raise ValueError("no POINTS in VTK file")
    polys, meta = polys_from_mesh(points, lines, pa, ca, ".vtk", lookup_from_field(fd))
    meta["field_data"] = {k: (list(v)[:30] if np.asarray(v).dtype == object else list(np.shape(v)))
                          for k, v in fd.items()}
    meta.update({"vtk_header": head, "vtk_keywords": dict(keywords)})
    return polys, meta


def parse_vtp_ascii(text):
    root = ET.fromstring(text)
    piece = root.find(".//Piece")
    if piece is None:
        raise ValueError("no Piece in VTP")

    def arr(el):
        if el.get("format", "ascii") != "ascii":
            raise ValueError("binary/appended VTP - install vtk (pip install vtk)")
        vals = (el.text or "").split()
        try:
            a = np.array(vals, float)
        except ValueError:
            a = np.array(vals, object)
        nc = int(el.get("NumberOfComponents", 1))
        return a.reshape(-1, nc) if nc > 1 else a

    pts = arr(piece.find("Points/DataArray")).reshape(-1, 3)
    lines = []
    le = piece.find("Lines")
    if le is not None:
        d = {a.get("Name"): arr(a) for a in le.findall("DataArray")}
        conn, offs = d["connectivity"].astype(int), d["offsets"].astype(int)
        start = 0
        for o in offs:
            lines.append(list(conn[start:o]))
            start = o
    pa = {a.get("Name"): arr(a) for a in piece.findall("PointData/DataArray")}
    ca = {a.get("Name"): arr(a) for a in piece.findall("CellData/DataArray")}
    return polys_from_mesh(pts, lines, pa, ca, ".vtp")


def _is_xyz_list(v):
    return (isinstance(v, list) and len(v) >= 2 and all(
        (isinstance(p, (list, tuple)) and 3 <= len(p) <= 4 and all(isinstance(c, (int, float)) for c in p))
        or (isinstance(p, dict) and all(k in {kk.lower() for kk in p} for k in "xyz"))
        for p in v[:50]))


def _label_of(d):
    if not isinstance(d, dict):
        return None
    for k, v in d.items():
        if label_like(k) and isinstance(v, (str, int)) and not isinstance(v, bool):
            return v
    return None


def parse_json(obj, source):
    out, keys_seen = [], Counter()

    def walk(o, key_path, inherited):
        if isinstance(o, dict):
            keys_seen.update(o.keys())
            lab = _label_of(o)
            lab = inherited if lab is None else lab
            for k, v in o.items():
                walk(v, key_path + [str(k)], lab)
        elif isinstance(o, list):
            if _is_xyz_list(o):
                named = [k for k in reversed(key_path) if k.lower() not in GENERIC_KEYS and not k.isdigit()]
                label = inherited if inherited is not None else (named[0] if named else None)
                pts, labels, rad = [], [], []
                for p in o:
                    if isinstance(p, dict):
                        low = {kk.lower(): vv for kk, vv in p.items()}
                        pts.append([low["x"], low["y"], low["z"]])
                        pl = _label_of(p)
                        labels.append(label if pl is None else pl)
                        r = next((vv for kk, vv in low.items() if any(h in kk for h in RADIUS_HINTS) or kk == "r"), None)
                        rad.append(np.nan if r is None else r)
                    else:
                        pts.append(p[:3])
                        labels.append(label)
                        rad.append(p[3] if len(p) == 4 else np.nan)
                rad = np.array(rad, float)
                out.append(Poly(pts, labels, None if np.isnan(rad).all() else rad, source))
            else:
                for j, v in enumerate(o):
                    walk(v, key_path + [str(j)], inherited)

    walk(obj, [], None)
    return out, {"json_keys": [k for k, _ in keys_seen.most_common(30)], "n_lines": len(out)}


def split_rows(df, source):
    """Polylines from a table with x/y/z columns (+ optional label / branch-id columns)."""
    cols = {c: str(c).strip().lower() for c in df.columns}

    def find(axis):
        pats = [rf"^{axis}$", rf"^{axis}[_\s(\[]", rf"^(pos|point|coord|p|world|centerline)[_\s]?{axis}$",
                rf"[_\s]{axis}$", rf"^{axis}\d*$"]
        for pat in pats:
            for c, low in cols.items():
                if re.search(pat, low):
                    return c
        return None

    xyz = [find(a) for a in "xyz"]
    if None in xyz or len(set(xyz)) < 3:
        num = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if len(num) < 3:
            raise ValueError(f"no x/y/z columns in {list(df.columns)[:12]}")
        xyz = num[:3]
    rest = {c: df[c].to_numpy() for c in df.columns if c not in xyz}
    lab = pick_label_array({c: v for c, v in rest.items()
                            if not re.search(r"(branch|line|path|cell|curve)", cols[c])})
    grp = next((c for c in rest if re.search(r"(branch|line|path|cell|curve|polyline).*(id|idx|index|nr|no)?$", cols[c])
                and c != lab), None)
    rad = pick_radius_array(rest)
    out = []
    groups = [df] if grp is None else [g for _, g in df.groupby(grp, sort=False)]
    for g in groups:
        pts = g[xyz].to_numpy(float)
        labels = g[lab].tolist() if lab else None
        r = g[rad].to_numpy(float) if rad else None
        out.append(Poly(pts, labels, r, source, explicit=False))
    meta = {"columns": [str(c) for c in df.columns][:30], "xyz": [str(c) for c in xyz],
            "label_array": lab, "group_column": grp, "n_lines": len(out)}
    return out, meta


def parse_xml(text, source):
    root = ET.fromstring(text)
    groups = defaultdict(list)
    for parent in root.iter():
        for el in parent:
            att = {k.lower(): v for k, v in el.attrib.items()}
            if all(a in att for a in "xyz"):
                groups[parent].append(el)
            else:
                kids = {c.tag.lower(): (c.text or "").strip() for c in el}
                if all(a in kids for a in "xyz"):
                    groups[parent].append(el)
    out = []
    for parent, els in groups.items():
        lab = _label_of({k: v for k, v in parent.attrib.items()}) or parent.tag
        pts, labels = [], []
        for el in els:
            att = {k.lower(): v for k, v in el.attrib.items()}
            kids = {c.tag.lower(): (c.text or "").strip() for c in el}
            src = att if all(a in att for a in "xyz") else kids
            pts.append([float(src["x"]), float(src["y"]), float(src["z"])])
            labels.append(_label_of(src) or lab)
        out.append(Poly(pts, labels, None, source, explicit=False))
    return out, {"xml_root": root.tag, "n_lines": len(out)}


def parse_member(name, data):
    e = ext(name)
    if e.endswith(".gz"):
        import gzip
        data, e = gzip.decompress(data), e[:-3]
    stem_label = Path(name).name.split(".")[0]
    if e == ".vtk":  # own reader first (ASCII and binary, VTK 4.x and 5.1); vtk package as backup
        try:
            polys, meta = parse_vtk_legacy(data)
        except Exception as ex:  # noqa: BLE001
            res = parse_vtk_lib(data, e)
            if res is None:
                raise ValueError(f"{ex} (and the vtk package is not installed)") from ex
            polys, meta = res
    elif e == ".vtp":
        res = parse_vtk_lib(data, e)
        polys, meta = res if res is not None else parse_vtp_ascii(data.decode("latin-1"))
    elif e == ".json":
        polys, meta = parse_json(json.loads(data.decode("utf-8-sig")), name)
    elif e in (".csv", ".txt", ".tsv", ".dat", ".ctl", ".cl"):
        text = data.decode("utf-8-sig", errors="replace")
        first = next((ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")), "")
        header = re.search(r"[A-Za-z]", first) is not None
        df = pd.read_csv(io.StringIO(text), sep=None, engine="python", comment="#",
                         header=0 if header else None)
        polys, meta = split_rows(df, name)
    elif e == ".xml":
        polys, meta = parse_xml(data.decode("utf-8-sig", errors="replace"), name)
    elif e in (".npy", ".npz"):
        z = np.load(io.BytesIO(data), allow_pickle=False)
        arrs = {stem_label: z} if e == ".npy" else dict(z)
        polys = [Poly(a[:, :3], [k] * len(a), a[:, 3] if a.shape[1] > 3 else None, name)
                 for k, a in arrs.items() if a.ndim == 2 and a.shape[1] in (3, 4)]
        meta = {"arrays": {k: list(a.shape) for k, a in arrs.items()}, "n_lines": len(polys)}
    else:
        raise ValueError(f"unsupported file type {e}")
    # a file with no labels inside: use the file name as the label (e.g. LAD.vtp)
    if all(l is None for p in polys for l in p.labels):
        for p in polys:
            p.labels = [stem_label] * len(p.pts)
        meta["label_from_filename"] = True
    return polys, meta


# ============================================================ labels
_numbering = None  # decided once over all cases ("scct" or "raw")
_code_names = {}  # code -> name, pooled over all files' segment_names (codes a file uses but does not name)


def norm_key(v):
    s = str(v).strip().lower()
    if re.fullmatch(r"-?\d+(\.0+)?", s):
        return str(int(float(s)))
    return re.sub(r"[\s_\-\.()/]+", "", s)


def normalise_label(v):
    """Raw label -> segment name, None (unlabelled) or '?raw' (not recognised)."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    m = re.match(r"^\s*-?\d+\s*:\s*(.+)$", str(v))  # "code:name" from a lookup: use the name
    if m:
        v = m.group(1)
    k = norm_key(v)
    if k in UNLABELLED:
        return None
    if k.lstrip("-").isdigit() and int(k) in _code_names:
        return normalise_label(_code_names[int(k)])
    if k.lstrip("-").isdigit():
        if _numbering == "scct" and int(k) in SCCT:
            return SCCT[int(k)]
        return f"#{k}"
    if k in ALIASES:
        return ALIASES[k]
    for alias in sorted(ALIASES, key=len, reverse=True):  # e.g. "seg_pLAD_v2", "LAD_centerline"
        if len(alias) >= 3 and re.search(rf"(^|[^a-z]){alias}($|[^a-z])", str(v).lower().replace("_", " ")):
            return ALIASES[alias]
    return f"?{str(v).strip()[:30]}"


def decide_numbering(raw_values):
    global _numbering
    if LABEL_NUMBERING != "auto":
        _numbering = LABEL_NUMBERING
        return
    nums = [int(norm_key(v)) for v in raw_values if norm_key(v).lstrip("-").isdigit()]
    _numbering = "scct" if nums and all(-1 <= n <= 18 for n in nums) else "raw"


# ============================================================ graph metrics
def nearest(query, ref):
    """Distance and index of the nearest ref point for each query point."""
    try:
        from scipy.spatial import cKDTree
        return cKDTree(ref).query(query)
    except ImportError:
        d = np.empty(len(query)); idx = np.empty(len(query), int)
        for s in range(0, len(query), 256):
            dd = np.linalg.norm(query[s:s + 256, None] - ref[None], axis=2)
            idx[s:s + 256] = dd.argmin(1); d[s:s + 256] = dd.min(1)
        return d, idx


def split_gaps(polys):
    out, n_gaps = [], 0
    for p in polys:
        if len(p.pts) < 2:
            continue
        step = np.linalg.norm(np.diff(p.pts, axis=0), axis=1)
        med = np.median(step) if len(step) else 0
        cut = np.where(step > max(GAP_MIN, GAP_FACTOR * med))[0]
        n_gaps += len(cut)
        if p.explicit:  # keep the file's connectivity; just count the jumps
            out.append(p)
            continue
        bounds = [0, *(cut + 1), len(p.pts)]
        for a, b in zip(bounds[:-1], bounds[1:]):
            if b - a >= 2:
                out.append(Poly(p.pts[a:b], p.labels[a:b], None if p.radius is None else p.radius[a:b],
                                p.source, p.explicit))
    return out, n_gaps


def analyse_case(polys):
    polys, n_gaps = split_gaps(polys)
    polys = [p for p in polys if len(p.pts) >= 2 and np.isfinite(p.pts).all()]
    if not polys:
        raise ValueError("no usable polyline (all empty or non-finite)")
    P = np.concatenate([p.pts for p in polys])
    L = [normalise_label(l) for p in polys for l in p.labels]
    pid = np.concatenate([np.full(len(p.pts), i) for i, p in enumerate(polys)])

    # nodes: points closer than DEDUP_TOL are one node
    key = np.round(P / DEDUP_TOL).astype(np.int64)
    _, node, counts = np.unique(key, axis=0, return_inverse=True, return_counts=True)
    node = node.ravel()
    n_nodes = node.max() + 1
    node_pts = np.zeros((n_nodes, 3)); node_pts[node] = P
    node_lab = [None] * n_nodes
    for i, l in enumerate(L):
        if node_lab[node[i]] is None:
            node_lab[node[i]] = l

    edges = set()
    start = 0
    for p in polys:
        idx = node[start:start + len(p.pts)]
        edges.update((min(a, b), max(a, b)) for a, b in zip(idx[:-1], idx[1:]) if a != b)
        start += len(p.pts)
    # join polyline ends to the nearest point of another polyline
    n_joined = 0
    starts = np.cumsum([0] + [len(p.pts) for p in polys])
    for i, p in enumerate(polys):
        other = pid != i
        if not other.any():
            continue
        for e_idx in (starts[i], starts[i + 1] - 1):
            d, j = nearest(P[e_idx][None], P[other])
            j = np.where(other)[0][j[0]] if np.ndim(j) else np.where(other)[0][j]
            d = float(np.ravel(d)[0])
            a, b = node[e_idx], node[j]
            if a != b and d <= JOIN_TOL:
                if (min(a, b), max(a, b)) not in edges:
                    n_joined += 1
                edges.add((min(a, b), max(a, b)))

    E = np.array(sorted(edges)) if edges else np.zeros((0, 2), int)
    deg = np.bincount(E.ravel(), minlength=n_nodes)
    elen = np.linalg.norm(node_pts[E[:, 0]] - node_pts[E[:, 1]], axis=1) if len(E) else np.zeros(0)

    # lengths per label (an edge between two labels is split half/half)
    seg_len = defaultdict(float)
    for (a, b), l in zip(E, elen):
        la, lb = node_lab[a], node_lab[b]
        seg_len[la] += l / 2
        seg_len[lb] += l / 2
    total = float(elen.sum())
    unl = seg_len.pop(None, 0.0)

    # connected components (union-find)
    parent = np.arange(n_nodes)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in E:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    roots = np.array([find(i) for i in range(n_nodes)])
    comp_len = defaultdict(float)
    for (a, _), l in zip(E, elen):
        comp_len[roots[a]] += l
    comp_labels = defaultdict(set)
    for i, l in enumerate(node_lab):
        if l:
            comp_labels[roots[i]].add(TERRITORY.get(l, l))
    comps = set(roots)
    tiny = sum(1 for c in comps if comp_len[c] < 10)
    left_right_joined = any({"LM", "RCA"} <= s or ({"LAD", "RCA"} <= s) for s in comp_labels.values())

    # label contacts: direct, and via a stretch of unlabelled nodes
    direct = Counter()
    for a, b in E:
        la, lb = node_lab[a], node_lab[b]
        if la and lb and la != lb:
            direct[frozenset((la, lb))] += 1
    adj = defaultdict(list)
    for a, b in E:
        adj[a].append(b); adj[b].append(a)
    via = set()
    seen = np.zeros(n_nodes, bool)
    for s in range(n_nodes):
        if node_lab[s] is not None or seen[s]:
            continue
        stack, touching = [s], set()
        seen[s] = True
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if node_lab[y] is None and not seen[y]:
                    seen[y] = True; stack.append(y)
                elif node_lab[y] is not None:
                    touching.add(node_lab[y])
        touching = sorted(touching)
        via.update(frozenset((x, y)) for i, x in enumerate(touching) for y in touching[i + 1:])

    # overlap between polylines (same path exported twice, or near-parallel copies)
    overlap = 0.0
    if len(polys) > 1:
        shared = counts[node] > 1
        for i, p in enumerate(polys):
            idx = np.arange(starts[i], starts[i + 1])
            other = pid != i
            d, _ = nearest(P[idx], P[other])
            cum = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(p.pts, axis=0), axis=1))])
            inner = (cum > 2.0) & (cum < cum[-1] - 2.0)
            ov = inner & ((np.ravel(d) <= OVERLAP_TOL) | shared[idx])
            step = np.diff(cum, prepend=0)
            overlap += float(step[ov].sum())

    spacing = np.concatenate([np.linalg.norm(np.diff(p.pts, axis=0), axis=1) for p in polys])
    radius = np.concatenate([p.radius for p in polys if p.radius is not None]) if any(
        p.radius is not None for p in polys) else np.zeros(0)
    labs = {l for l in node_lab if l}
    ext_ = P.max(0) - P.min(0)
    m = {
        "n_polylines": len(polys), "n_points": len(P), "n_nodes": int(n_nodes),
        "total_mm": round(total, 2), "unlabelled_mm": round(unl, 2),
        "unlabelled_pct": round(100 * unl / total, 2) if total else np.nan,
        "n_components": len(comps), "n_tiny_components": tiny,
        "n_branch_points": int((deg >= 3).sum()), "n_end_points": int((deg == 1).sum()),
        "max_degree": int(deg.max()) if len(deg) else 0,
        "n_isolated_points": int((deg == 0).sum()),
        "n_gaps": n_gaps, "n_joins": n_joined, "overlap_mm": round(overlap, 2),
        "median_spacing_mm": round(float(np.median(spacing)), 4),
        "max_spacing_mm": round(float(spacing.max()), 3),
        "extent_x": round(float(ext_[0]), 1), "extent_y": round(float(ext_[1]), 1),
        "extent_z": round(float(ext_[2]), 1),
        "median_radius": round(float(np.nanmedian(radius)), 3) if len(radius) else np.nan,
        "unknown_labels": ";".join(sorted(l for l in labs if l[0] in "?#")),
        "left_right_joined": left_right_joined,
    }
    for c, parents in EXPECTED:
        if c not in labs or not (parents & labs):
            m[f"conn_{c}"] = "n/a"
            continue
        if any(frozenset((c, p)) in direct for p in parents):
            m[f"conn_{c}"] = "direct"
        elif any(frozenset((c, p)) in via for p in parents):
            m[f"conn_{c}"] = "via_unlabelled"
        else:
            m[f"conn_{c}"] = "missing"
    unexpected = sorted("-".join(sorted(pair)) for pair in set(direct) | via
                        if pair not in EXPECTED_PAIRS and not all(x[0] in "?#" for x in pair))
    m["unexpected_contacts"] = ";".join(unexpected)
    m["impossible_contacts"] = ";".join(
        "-".join(sorted(pair)) for pair in set(direct) | via
        if frozenset(TERRITORY.get(x, x) for x in pair) in IMPOSSIBLE)
    return m, dict(seg_len)


def flags_for(m, seg):
    has = lambda group: any(seg.get(s, 0) > 0 for s in group)
    f = []
    if not has({"LM"}): f.append("no_LM")
    if not has(LAD): f.append("no_LAD")
    if not has(CX): f.append("no_CX")
    if not has(RCA): f.append("no_RCA")
    if m["unlabelled_pct"] > 20: f.append("unlabelled>20%")
    if m["n_components"] > 2: f.append(">2_components")
    if m["n_components"] == 1 and has(RCA) and has(LAD | {"LM"}): f.append("left_and_right_in_one_tree")
    if m["left_right_joined"]: f.append("left_right_labels_joined")
    if m["impossible_contacts"]: f.append("impossible_contact")
    if any(v == "missing" for k, v in m.items() if k.startswith("conn_")): f.append("disconnected_segment")
    if any(0 < seg.get(s, 0) < SHORT_SEGMENT for s in SEGMENTS): f.append(f"segment<{SHORT_SEGMENT:g}mm")
    if m["n_gaps"]: f.append("gaps_in_polyline")
    if m["unknown_labels"]: f.append("unknown_labels")
    if m["total_mm"] < 50 or m["total_mm"] > 2000: f.append("total_length_odd(units?)")
    if m["overlap_mm"] > 0.2 * m["total_mm"]: f.append("overlapping_polylines")
    return f


# ============================================================ reporting helpers
def dist(x):
    x = pd.Series(x, dtype=float).dropna()
    if x.empty:
        return {"n": 0}
    q = x.quantile([0, .05, .25, .5, .75, .95, 1]).round(1).tolist()
    return {"n": len(x), "mean": round(x.mean(), 1), "min": q[0], "p5": q[1], "q1": q[2],
            "median": q[3], "q3": q[4], "p95": q[5], "max": q[6]}


def md_table(df):
    df = df.fillna("")
    cols = [str(c) for c in df.columns]
    rows = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    rows += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(rows)


def peek(src, name, n_lines=15):
    """First lines (text) or structure (binary) of one file, for the inventory."""
    data = src.read(name)
    e = ext(name)
    out = [f"### `{name}` ({len(data):,} bytes)"]
    try:
        polys, meta = parse_member(name, data)
        out.append(f"parsed: {len(polys)} polylines, {sum(len(p.pts) for p in polys):,} points; "
                   f"meta: `{json.dumps(meta, default=str)[:800]}`")
        raw = Counter(str(l) for p in polys for l in p.labels)
        out.append(f"raw label values (count of points): `{dict(raw.most_common(25))}`")
    except Exception as ex:  # noqa: BLE001 - reported, not fatal
        out.append(f"**could not parse**: {type(ex).__name__}: {ex}")
    if e in TEXT_EXT or (not e.endswith(".gz") and data[:200].isascii()):
        text = []
        for ln in data[:20000].decode("latin-1").splitlines()[:n_lines]:
            if any(ord(c) < 9 or 13 < ord(c) < 32 or ord(c) > 126 for c in ln):
                text.append("... (binary data follows)")
                break
            text.append(ln[:200])
        out.append("```\n" + "\n".join(text) + "\n```")
    return "\n\n".join(out)


def inventory(src, cases, mode, root):
    exts = Counter(ext(m) for m in src.members)
    per_case = Counter(len(v) for v in cases.values())
    depth = Counter(m.count("/") for m in src.members)
    lines = [
        "# Centerline inventory", "",
        f"Source: `{src.path}`", "",
        f"- files: {len(src.members):,} (after skipping {', '.join(SKIP)})",
        f"- common root folder: `{root or '(none)'}`",
        f"- cases: {len(cases):,} (one per {mode}); expected {EXPECTED_CASES}",
        f"- files per case: {dict(sorted(per_case.items()))}",
        f"- folder depth of files: {dict(sorted(depth.items()))}",
        f"- file types: {dict(exts.most_common())}", "",
        "Example paths:", "", "```", *src.members[:15], "```", "",
        "Example case IDs: " + ", ".join(f"`{c}`" for c in list(cases)[:10]), "",
        "File names within cases (most common, case ID removed):", "",
    ]
    names = Counter()
    for cid, ms in cases.items():
        for m in ms:
            names[Path(m).name.replace(cid, "<case>")] += 1
    lines += [f"- `{k}`: {v}" for k, v in names.most_common(25)]
    lines += ["", "## One example file per type", ""]
    for e in exts:
        example = next(m for m in src.members if ext(m) == e)
        if e in PARSEABLE or e.endswith(".gz"):
            lines.append(peek(src, example))
        else:  # e.g. a processing log: not a case, but show its start
            data = src.read(example)
            text = data[:20000].decode("utf-8", errors="replace").splitlines()[:40]
            lines.append(f"### `{example}` ({len(data):,} bytes, not a centerline file - first lines)\n\n"
                         "```\n" + "\n".join(ln[:200] for ln in text) + "\n```")
        lines.append("")
    return "\n".join(lines)


TRUNKS = {  # dominance-independent trunks; segments in order, each joined to the one before it
    "LAD": ["LM", "pLAD", "mLAD", "dLAD"],
    "CX": ["LM", "pCX", "CX"],
    "RCA": ["pRCA", "mRCA", "dRCA"],
    "RCA_no_dRCA": ["pRCA", "mRCA"],
}


def complete_trunks(df, seg):
    """Boolean columns complete_<trunk> and complete_trunks, one value per case (rows of df)."""
    n = len(df)
    s = seg.reindex(df["case"]).fillna(0)
    ok = lambda x: (s[x] > 0).to_numpy() if x in s.columns else np.zeros(n, bool)
    joined = lambda x: df[f"conn_{x}"].isin(["direct", "via_unlabelled"]).to_numpy() if f"conn_{x}" in df else np.zeros(n, bool)
    out = {f"complete_{k}": np.logical_and.reduce([ok(x) for x in v] + [joined(x) for x in v[1:]])
           for k, v in TRUNKS.items()}
    rca = out["complete_RCA"] if COMPLETE_RCA_NEEDS_DRCA else out["complete_RCA_no_dRCA"]
    out["complete_trunks"] = out["complete_LAD"] & out["complete_CX"] & rca
    return pd.DataFrame(out, index=df.index)


def write_id_lists(df, out):
    """complete_trunks.txt (all three trunks complete) and one list per trunk, one case ID per line."""
    rca_rule = "pRCA -> mRCA -> dRCA" if COMPLETE_RCA_NEEDS_DRCA else "pRCA -> mRCA (dRCA not required)"
    lists = {
        "complete_trunks.txt": ("complete_trunks", "LAD, CX and RCA trunks all complete: LM -> pLAD -> mLAD -> dLAD, "
                           f"LM -> pCx -> LCx, {rca_rule}"),
        "complete_LAD.txt": ("complete_LAD", "LAD trunk complete: LM -> pLAD -> mLAD -> dLAD"),
        "complete_CX.txt": ("complete_CX", "CX trunk complete: LM -> pCx -> LCx"),
        "complete_RCA.txt": ("complete_RCA", "RCA trunk complete: pRCA -> mRCA -> dRCA"),
        "complete_RCA_no_dRCA.txt": ("complete_RCA_no_dRCA", "RCA trunk complete without dRCA: pRCA -> mRCA"),
    }
    for fn, (col, rule) in lists.items():
        ids = df.loc[df[col], "case"].astype(str).tolist()
        head = [f"# {rule}",
                "# complete = every segment present and joined to the one before it (directly or via unlabelled points)",
                f"# {len(ids)} of {len(df)} cases", ""]
        (out / fn).write_text("\n".join(head + ids) + "\n", encoding="utf-8")


def plots(df, seg, out, sub="all", title=""):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available - skipping figures")
        return
    fig_dir = out / "figures" / sub
    fig_dir.mkdir(parents=True, exist_ok=True)
    seg = seg.reindex(df["case"]).fillna(0)
    title = f"{title} (n = {len(df)} cases)"
    blue = "#2a6fb0"
    present = [s for s in SEGMENTS if s in seg.columns and seg[s].gt(0).any()]
    others = sorted(c for c in seg.columns if c not in SEGMENTS)
    cols = present + others
    if cols:
        n = len(cols)
        nc = 4
        nr = int(np.ceil(n / nc))
        fig, axes = plt.subplots(nr, nc, figsize=(4 * nc, 2.6 * nr), squeeze=False)
        for ax, s in zip(axes.ravel(), cols):
            x = seg[s][seg[s] > 0]
            ax.hist(x, bins=30, color=blue, edgecolor="white", linewidth=0.5)
            ax.set_title(f"{s}  (n={len(x)}, median {x.median():.0f} mm)", fontsize=9)
            ax.set_xlabel("length (mm)", fontsize=8)
            ax.tick_params(labelsize=7)
            ax.spines[["top", "right"]].set_visible(False)
        for ax in axes.ravel()[n:]:
            ax.axis("off")
        fig.suptitle(title, fontsize=11)
        fig.tight_layout()
        fig.savefig(fig_dir / "segment_lengths.png", dpi=130)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(max(6, 0.45 * len(cols)), 3.2))
        pres = 100 * seg[cols].gt(0).sum() / len(seg)
        ax.bar(range(len(cols)), pres, color=blue, width=0.7)
        ax.set_xticks(range(len(cols)), cols, rotation=60, fontsize=7, ha="right")
        ax.set_ylabel("% of cases with segment")
        ax.set_ylim(0, 100)
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        fig.savefig(fig_dir / "segment_presence.png", dpi=130)
        plt.close(fig)

    for col, xl, fn in (("unlabelled_pct", "unlabelled length (% of total)", "unlabelled_pct"),
                        ("n_branch_points", "branch points per case", "branch_points"),
                        ("total_mm", "total centerline length (mm)", "total_length"),
                        ("n_components", "connected components per case", "components")):
        x = df[col].dropna()
        if x.empty:
            continue
        fig, ax = plt.subplots(figsize=(5, 3))
        discrete = col in ("n_branch_points", "n_components")
        bins = np.arange(x.min() - 0.5, x.max() + 1.5) if discrete and x.max() - x.min() < 60 else 30
        ax.hist(x, bins=bins, color=blue, edgecolor="white", linewidth=0.5)
        ax.set_xlabel(xl)
        ax.set_ylabel("cases")
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        fig.savefig(fig_dir / f"{fn}.png", dpi=130)
        plt.close(fig)


# ============================================================ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=ZIP_PATH, help="zip file or folder with the centerlines")
    ap.add_argument("--out", default=OUT_DIR, help="output folder")
    ap.add_argument("--inspect", action="store_true", help="only write inventory.md")
    ap.add_argument("--limit", type=int, default=None, help="only analyse the first N cases")
    args = ap.parse_args()

    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    src = Source(args.src)
    cases, mode, root = group_cases(src.members)
    print(f"{len(src.members):,} files, {len(cases):,} cases (one per {mode})")

    inv = inventory(src, cases, mode, root)
    (out / "inventory.md").write_text(inv, encoding="utf-8")
    print(f"wrote {out / 'inventory.md'}")
    if args.inspect:
        print(inv)
        return

    items = list(cases.items())[: args.limit] if args.limit else list(cases.items())
    parsed, errors, metas, raw_counter = {}, {}, Counter(), Counter()
    code_use = defaultdict(lambda: {"names": Counter(), "files": 0, "unnamed": 0, "points": 0})
    for k, (cid, ms) in enumerate(items, 1):
        polys, errs = [], []
        for m in ms:
            if ext(m) not in PARSEABLE and not ext(m).endswith(".gz"):
                continue
            try:
                p, meta = parse_member(m, src.read(m))
                polys += p
                count_codes(p, meta, code_use)
                metas[json.dumps({k_: v for k_, v in meta.items() if k_ != "n_lines"}, sort_keys=True, default=str)[:400]] += 1
            except Exception as ex:  # noqa: BLE001 - collected and reported
                errs.append(f"{Path(m).name}: {type(ex).__name__}: {ex}"[:300])
        if polys:
            parsed[cid] = polys
            raw_counter.update(str(l) for p in polys for l in p.labels)
        if errs or not polys:
            errors[cid] = errs or ["no parseable centerline file"]
        if k % 50 == 0:
            print(f"  read {k}/{len(items)}")

    decide_numbering(raw_counter)
    for c, u in code_use.items():  # most common name per code, over the files that name it
        if u["names"]:
            _code_names[c] = u["names"].most_common(1)[0][0]
    _code_names.update(CODE_NAMES)
    rows, seg_rows = [], []
    for k, (cid, polys) in enumerate(parsed.items(), 1):
        try:
            m, seg = analyse_case(polys)
        except Exception as ex:  # noqa: BLE001
            errors.setdefault(cid, []).append(f"analysis: {type(ex).__name__}: {ex}"[:300])
            continue
        m["flags"] = ";".join(flags_for(m, seg))
        rows.append({"case": cid, **m})
        seg_rows += [{"case": cid, "segment": s, "length_mm": round(v, 2)} for s, v in seg.items()]
        if k % 50 == 0:
            print(f"  analysed {k}/{len(parsed)}")

    df = pd.DataFrame(rows)
    seg_long = pd.DataFrame(seg_rows, columns=["case", "segment", "length_mm"])
    seg = (seg_long.pivot_table(index="case", columns="segment", values="length_mm", aggfunc="sum")
           .reindex(df["case"] if len(df) else []).fillna(0))
    if len(df):
        df = pd.concat([df, complete_trunks(df, seg)], axis=1)
        write_id_lists(df, out)
    df.to_csv(out / "per_case.csv", index=False)
    seg_long.to_csv(out / "segment_lengths.csv", index=False)
    lv = pd.DataFrame([(raw, normalise_label(raw if raw != "None" else None), n)
                       for raw, n in raw_counter.most_common()], columns=["raw_label", "mapped_to", "n_points"])
    lv.to_csv(out / "label_values.csv", index=False)
    if len(df):
        plots(df, seg, out, "all", "All centerlines")
        sub_df = df[df["complete_trunks"]]
        if len(sub_df):
            plots(sub_df, seg, out, "complete_trunks", "Complete trunks only")
        else:
            print("no case has all three trunks complete - figures/complete_trunks/ not made "
                  "(see the 'Complete main trunks' table in report.md)")
        print(f"complete trunks: {len(sub_df)} of {len(df)} cases")

    codes = pd.DataFrame([{"code": c, "names in segment_names (files)": "; ".join(f"{n} ({k})" for n, k in u["names"].most_common()),
                           "used as": normalise_label(c) or "(unlabelled)", "files using it": u["files"],
                           "files not naming it": u["unnamed"], "points": u["points"]}
                          for c, u in sorted(code_use.items())])
    codes.to_csv(out / "label_codes.csv", index=False)
    write_report(out, src, cases, items, df, seg, lv, errors, metas, codes)
    print(f"wrote {out / 'report.md'} and CSVs/figures in {out}")


def count_codes(polys, meta, code_use):
    """Per file: which integer label codes are used, and are they named in its own segment_names."""
    lookup = {}
    for v in meta.get("field_data", {}).values():
        if isinstance(v, list) and v and all(isinstance(x, str) for x in v):
            lookup.update(lookup_from_field({"x": v}) or {})
    used = Counter()
    for p in polys:
        for l in p.labels:
            m = re.match(r"^\s*(-?\d+)\s*:", str(l))
            if m:
                used[int(m.group(1))] += 1
            elif isinstance(l, (int, float, np.number)) and l == l and float(l).is_integer():
                used[int(l)] += 1
    for c, n in used.items():
        u = code_use[c]
        u["files"] += 1
        u["points"] += n
        if c in lookup:
            u["names"][lookup[c].split(":", 1)[1]] += 1
        else:
            u["unnamed"] += 1


def write_report(out, src, cases, items, df, seg, lv, errors, metas, codes=None):
    n = len(df)
    R = ["# Centerline quality report", "",
         f"Source `{src.path}`: {len(cases)} cases found (expected {EXPECTED_CASES}), "
         f"{len(items)} read, **{n} analysed**, {len(errors)} with read errors.", "",
         f"Settings: JOIN_TOL {JOIN_TOL} mm, DEDUP_TOL {DEDUP_TOL} mm, gap > max({GAP_MIN} mm, "
         f"{GAP_FACTOR}x median spacing), numeric labels read as: **{_numbering}**.", ""]
    if metas:
        R += ["## How the files were read", "",
              "Most common parse results (arrays/columns found, which one was used as label):", ""]
        R += [f"- {c} files: `{k}`" for k, c in metas.most_common(8)]
        R.append("")
    if codes is not None and len(codes):
        R += ["## Label codes", "",
              "Integer codes in the label array. Each file names only some codes in its own "
              "`segment_names`; a code a file uses without naming it gets the name other files give "
              "it (most common). Codes no file names stay `#n` - ask Kit what they are.", "",
              md_table(codes), ""]
    R += ["## Label values", "",
          "Raw labels and the segment they were mapped to (`?x` = not recognised, `#n` = number "
          "not mapped, empty = unlabelled). **Check this first** - all other numbers depend on it.", "",
          md_table(lv.head(60)), ""]
    if not n:
        R += ["No case could be analysed. See inventory.md and the errors below."]
    else:
        R += ["## Overview per case", ""]
        R.append(md_table(pd.DataFrame({c: dist(df[c]) for c in (
            "total_mm", "unlabelled_mm", "unlabelled_pct", "n_polylines", "n_points",
            "n_branch_points", "n_end_points", "max_degree", "n_components", "n_tiny_components",
            "n_gaps", "n_joins", "overlap_mm", "median_spacing_mm", "max_spacing_mm",
            "extent_x", "extent_y", "extent_z", "median_radius")}).T.reset_index().rename(columns={"index": "metric"})))
        R += ["", "Units: total lengths of ~200-800 mm and extents of ~50-150 mm mean mm; "
              "much smaller values suggest cm, much larger voxels.", "",
              f"Unlabelled length over all cases: {df['unlabelled_mm'].sum():.0f} of "
              f"{df['total_mm'].sum():.0f} mm (**{100 * df['unlabelled_mm'].sum() / df['total_mm'].sum():.1f} %**); "
              f"cases with any unlabelled length: {(df['unlabelled_mm'] > 0).sum()} of {n}.", ""]
        ct = pd.DataFrame({"all cases": df["n_components"].value_counts(),
                           "complete trunks": df.loc[df["complete_trunks"], "n_components"].value_counts(),
                           "complete trunks, pieces < 10 mm ignored":
                               (df["n_components"] - df["n_tiny_components"])[df["complete_trunks"]].value_counts()})
        R += ["Connected components (separate pieces) per case - expect 2: left and right tree. In complete-trunk "
              "cases the LAD/CX trunks are one piece and the RCA trunk another, so extra pieces are side branches "
              "or fragments:", "",
              md_table(ct.fillna(0).astype(int).sort_index().rename_axis("components").reset_index()), ""]

        R += ["## Segments: presence and length (mm)", ""]
        cols = [s for s in SEGMENTS if s in seg.columns] + sorted(c for c in seg.columns if c not in SEGMENTS)
        tab = []
        for s in cols:
            x = seg[s][seg[s] > 0]
            tab.append({"segment": s, "cases": len(x), "% cases": round(100 * len(x) / n, 1), **{
                k: v for k, v in dist(x).items() if k != "n"}})
        R += [md_table(pd.DataFrame(tab)), ""]
        has = lambda g: seg[[c for c in g if c in seg.columns]].gt(0).any(axis=1) if any(c in seg.columns for c in g) else pd.Series(False, index=seg.index)
        R += ["Whole arteries present (any of their segments):", ""]
        R += [f"- {name}: {int(has(g).sum())} of {n} ({100 * has(g).mean():.1f} %)"
              for name, g in (("LM", {"LM"}), ("LAD", LAD), ("CX", CX), ("RCA", RCA))]
        R += ["", "## Complete main trunks (not dominance-dependent)", "",
              "A trunk is complete when all its segments are present and each is joined to the one "
              "before it (directly or through unlabelled points). PDA/PLB are left out as they depend "
              "on dominance; dRCA can be small in left-dominant hearts, so RCA is also shown without it.", ""]
        rows_ = [("LM + LAD (LM, pLAD, mLAD, dLAD)", df["complete_LAD"]),
                 ("LM + CX (LM, pCx, LCx)", df["complete_CX"]),
                 ("RCA (pRCA, mRCA, dRCA)", df["complete_RCA"]),
                 ("RCA without dRCA (pRCA, mRCA)", df["complete_RCA_no_dRCA"]),
                 ("All three (LAD, CX, RCA incl. dRCA)", df["complete_LAD"] & df["complete_CX"] & df["complete_RCA"]),
                 ("All three, RCA without dRCA", df["complete_LAD"] & df["complete_CX"] & df["complete_RCA_no_dRCA"])]
        R += md_table(pd.DataFrame([{"trunk": k, "complete cases": int(v.sum()), "% of cases": round(100 * v.mean(), 1)}
                                    for k, v in rows_])).splitlines()
        rule = "incl. dRCA" if COMPLETE_RCA_NEEDS_DRCA else "RCA without dRCA"
        R += ["", f"**Complete trunks** (all three, {rule}; set by COMPLETE_RCA_NEEDS_DRCA): {int(df['complete_trunks'].sum())} of {n}. "
              "Case IDs: `complete_trunks.txt`; per trunk: `complete_LAD.txt`, `complete_CX.txt`, `complete_RCA.txt`, "
              "`complete_RCA_no_dRCA.txt`. Figures: `figures/all/` (all centerlines) and `figures/complete_trunks/`."]
        R += ["", "## Expected connections", "",
              "Among cases that have both the segment and one of its parents: `direct` = an edge joins "
              "them, `via_unlabelled` = joined through unlabelled points, `missing` = not joined "
              f"(a gap > {JOIN_TOL} mm or the segment hangs elsewhere).", ""]
        conn = []
        for c, parents in EXPECTED:
            col = f"conn_{c}"
            if col not in df:
                continue
            vc = df[col].value_counts()
            k = int(vc.drop("n/a", errors="ignore").sum())
            if k:
                conn.append({"segment": c, "parent(s)": "/".join(sorted(parents)), "cases": k,
                             **{v: int(vc.get(v, 0)) for v in ("direct", "via_unlabelled", "missing")}})
        R += [md_table(pd.DataFrame(conn)) if conn else "(no labelled segment pairs found)", ""]
        un = Counter(x for s in df["unexpected_contacts"] for x in s.split(";") if x)
        R += ["Unexpected segment contacts (pairs not in the expected list; number of cases):", ""]
        R += [f"- {k}: {v}" for k, v in un.most_common(30)] or ["- none"]
        R.append("")

        R += ["## Red flags", ""]
        fl = Counter(f for s in df["flags"] for f in s.split(";") if f)
        R += [f"Cases without any flag: {(df['flags'] == '').sum()} of {n}.", "",
              md_table(pd.DataFrame([(f, c) for f, c in fl.most_common()], columns=["flag", "cases"]))
              if fl else "none", ""]
        for f, _ in fl.most_common():
            ids = df.loc[df["flags"].str.split(";").apply(lambda l: f in l), "case"].tolist()
            R.append(f"- **{f}** ({len(ids)}): " + ", ".join(map(str, ids[:40])) + (" ..." if len(ids) > 40 else ""))
        R.append("")
        R += ["Flag meanings: `no_LM/LAD/CX/RCA` = artery missing (a missing LM can be real - separate "
              "ostia - but check); `unlabelled>20%`; `>2_components` = fragments; "
              "`left_and_right_in_one_tree` = left and right trees joined (should be separate); "
              "`impossible_contact` = e.g. LAD touching RCA; `disconnected_segment` = an expected "
              f"connection is missing; `segment<{SHORT_SEGMENT:g}mm`; `gaps_in_polyline` = jump inside "
              "one polyline; `unknown_labels` = labels not mapped (see label table); "
              "`overlapping_polylines` = > 20 % of length runs on top of another polyline.", ""]
        R += ["Figures in `figures/all/` and `figures/complete_trunks/`: `segment_lengths.png`, `segment_presence.png`, `unlabelled_pct.png`, "
              "`branch_points.png`, `total_length.png`, `components.png`.", ""]
    if errors:
        R += ["## Read / analysis errors", ""]
        err_types = Counter(re.sub(r"^[^:]*: ", "", e)[:120] for es in errors.values() for e in es)
        R += [f"- {c} x `{e}`" for e, c in err_types.most_common(15)]
        R += ["", "Cases: " + ", ".join(list(errors)[:40]) + (" ..." if len(errors) > 40 else ""), ""]
    if len(cases) != EXPECTED_CASES:
        R += [f"Note: {len(cases)} cases found but {EXPECTED_CASES} expected - check CASE_FROM / "
              "the inventory (several files per case, or extra files).", ""]
    (out / "report.md").write_text("\n".join(R), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
