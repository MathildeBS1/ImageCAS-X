"""Show the format of the tracer's lumen predictions, so the daughter asymmetry can be read from them.

    python CGPS_data/thesis_final/lumen_probe.py [--src PREDICTION_FOLDER] [--n 3]

Folder (Kit, 2026-11-19): /data/kimbr/predictions_CGPS-10Y_folds_01234, per scan <visit>_<id>.{
lumen_surface, outer_surface}[_ostium_pruned].vtk, .npz, .pkl, .ostia.json, .{3,16,29}cls[_ostium_pruned].nii.gz
and its own coronary_{left,right}_centerline[_ostium_pruned].vtk. Prints:
  the file kinds and their counts per visit;
  how many Medis participants have BL lumen contours, and how many have one named after the proximal LAD
  (plad or lad) and one after the proximal LCx (pcx or cx), an upper bound for the asymmetry comparison;
  for --n BL participants with a Medis tree and Medis lumen contours: the lumen surface and the centerline
  (show_file of tracer_probe), the keys, shapes and dtypes of the .npz, the structure of the .pkl (types,
  keys and shapes, no values), the .ostia.json; whether the centerlines equal those of tracer_io.TRACER_DIR;
  and the frame: the distance from the Medis lumen ring points to the nearest lumen surface vertex.
Participants are printed as 1, 2, 3; no study_id leaves the server. Reads only; the printout is also
written to lumen_probe.md next to this script.
"""
import argparse
import io
import json
import pickle
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
sys.path.insert(0, str(Path(__file__).resolve().parent))
import centerline_qc as cq
import hoe10y_qc as hq
from daughter_ratio import contour_diameter
from tracer_probe import Tee, bounds, describe_array, show_file

PRED_DIR = "/data/kimbr/predictions_CGPS-10Y_folds_01234"
PROX = {"LAD": {"plad", "lad"}, "CX": {"pcx", "cx"}}


def structure(x, depth=0, max_depth=3):
    """Lines describing the types, keys and shapes of x, no values."""
    pad = "    " + "  " * depth
    if isinstance(x, np.ndarray):
        return [f"{pad}ndarray {x.dtype} {x.shape}"]
    if isinstance(x, dict):
        out = [f"{pad}dict, {len(x)} keys"]
        for k in list(x)[:25] if depth < max_depth else []:
            out += [f"{pad}  [{k!r}]"] + structure(x[k], depth + 2, max_depth)
        return out
    if isinstance(x, (list, tuple)):
        out = [f"{pad}{type(x).__name__}, length {len(x)}"]
        if x and depth < max_depth:
            out += [f"{pad}  first element:"] + structure(x[0], depth + 2, max_depth)
            kinds = Counter(type(v).__name__ for v in x)
            out.append(f"{pad}  element types: {dict(kinds)}")
        return out
    if hasattr(x, "shape"):
        return [f"{pad}{type(x).__name__} {getattr(x, 'dtype', '')} {tuple(x.shape)}"]
    return [f"{pad}{type(x).__name__}"]


def npz_headers(path):
    """{array name: (shape, dtype)} from the .npy headers inside an .npz, without loading or unpickling data."""
    import zipfile

    out = {}
    with zipfile.ZipFile(path) as zf:
        for member in zf.namelist():
            with zf.open(member) as f:
                version = np.lib.format.read_magic(f)
                shape, _, dtype = (np.lib.format.read_array_header_1_0 if version == (1, 0)
                                   else np.lib.format.read_array_header_2_0)(f)
            out[member.removesuffix(".npy")] = (shape, dtype)
    return out


def lines_of(path):
    """Points of each LINES cell of a centerline file."""
    v = cq.read_vtk_legacy(Path(path).read_bytes())
    return np.concatenate([v["points"][np.asarray(c)] for c in v["cells"].get("LINES", [])])


def probe(args):
    import tracer_io
    from split_check import contour_files

    src = Path(args.src)
    files = sorted(src.glob("*_*.*"))
    kinds = Counter((p.name.split("_", 1)[0], p.name.split(".", 1)[1]) for p in files if p.name[:3] in ("BL_", "FU_"))
    print(f"{len(files)} files in {src}")
    for visit in ("BL", "FU"):
        print(f"  {visit}: " + ", ".join(f"{k} {n}" for (v, k), n in sorted(kinds.items()) if v == visit))
    other = sorted({p.name for p in src.iterdir()} - {p.name for p in files if p.name[:3] in ("BL_", "FU_")})
    print(f"  other entries: {', '.join(other)}")
    lumen = {hq.id_from_name(p.name.split(".", 1)[0]) for p in src.glob("BL_*.lumen_surface_ostium_pruned.vtk")}

    medis = {hq.id_from_name(p.name): p for p in tracer_io.MEDIS_TREES.rglob("*.vtk")}
    contours = contour_files(args.medis)
    with_lumen = {}
    for (pid, seg), fs in contours.items():
        if "lumen" in fs:
            with_lumen.setdefault(pid, set()).add(seg)
    both_prox = {p for p, segs in with_lumen.items() if segs & PROX["LAD"] and segs & PROX["CX"]}
    print("\nParticipants:")
    print(f"  BL lumen surface predicted                       {len(lumen)}")
    print(f"  Medis trees                                       {len(medis)}")
    print(f"    with a predicted BL lumen                       {len(set(medis) & lumen)}")
    print(f"  with BL Medis lumen contours                      {len(with_lumen)}")
    print(f"    and a Medis tree and a predicted lumen          {len(set(with_lumen) & set(medis) & lumen)}")
    print(f"  with Medis lumen named pLAD/LAD and pCx/LCx       {len(both_prox)}")
    print(f"    and a Medis tree and a predicted lumen          {len(both_prox & set(medis) & lumen)}")
    print("  (an upper bound: whether the contours cover 5-10 mm from O is decided after the trees are divided)\n")

    order = sorted(both_prox & set(medis) & lumen, key=int) or sorted(set(with_lumen) & set(medis) & lumen, key=int)
    for k, pid in enumerate(order[: args.n], 1):
        print(f"=== participant {k}")
        try:
            base = src / f"BL_{pid}"
            for kind in ("lumen_surface_ostium_pruned.vtk", "lumen_surface.vtk", "outer_surface_ostium_pruned.vtk",
                         "coronary_left_centerline_ostium_pruned.vtk"):
                p = Path(f"{base}.{kind}")
                if p.exists():
                    show_file(p)
                else:
                    print(f"  {kind}: missing")
            p = Path(f"{base}.npz")
            if p.exists():
                print(f"  npz: {len(npz_headers(p))} arrays")
                z = np.load(p, allow_pickle=False)
                for name, (shape, dtype) in npz_headers(p).items():
                    print(f"    {name}: dtype {dtype}, shape {shape}")
                    if dtype.hasobject or not 0 < np.prod(shape) <= 10 ** 6:
                        continue  # object arrays are not unpickled; large arrays only by shape
                    try:
                        a = z[name]
                        print(describe_array(name, a) if a.ndim else f"      value {a}")
                        if np.issubdtype(a.dtype, np.number):
                            print(f"      min {np.nanmin(a):.4g}, max {np.nanmax(a):.4g}")
                    except Exception as ex:  # noqa: BLE001 - shown
                        print(f"      not read ({type(ex).__name__}: {ex})")
            p = Path(f"{base}.pkl")
            if p.exists():
                try:
                    with open(p, "rb") as f:
                        obj = pickle.load(f)  # Kit's own output on this server
                    print("  pkl:")
                    print("\n".join(structure(obj)))
                except Exception as ex:  # noqa: BLE001 - shown
                    print(f"  pkl: not read ({type(ex).__name__}: {ex})")
            p = Path(f"{base}.ostia.json")
            if p.exists():
                print(f"  ostia.json: {json.dumps(json.loads(p.read_text()))[:600]}")

            for side in tracer_io.SIDES:  # same centerlines as the files the comparison reads so far?
                new = Path(f"{base}.coronary_{side}_centerline_ostium_pruned.vtk")
                old = Path(tracer_io.TRACER_DIR) / new.name
                if new.exists() and old.exists():
                    A, B = lines_of(new), lines_of(old)
                    d = np.ravel(cq.nearest(A, B)[0])
                    print(f"  {side} centerline against {tracer_io.TRACER_DIR}: {len(A)} / {len(B)} points, distance new to "
                          f"old median {np.median(d):.3f}, max {d.max():.3f} mm")
                else:
                    print(f"  {side} centerline: not in both folders")

            surf = Path(f"{base}.lumen_surface_ostium_pruned.vtk")
            if surf.exists():
                S = cq.read_vtk_legacy(surf.read_bytes())["points"]
                for seg in sorted(with_lumen.get(pid, ())):
                    fs = contours[(pid, seg)]
                    cl = cq.read_vtk_legacy(fs["centerline"].read_bytes())["points"] if "centerline" in fs else None
                    rings, how = hq.read_rings(fs["lumen"], cl)
                    R = np.concatenate(rings)
                    d = np.ravel(cq.nearest(R, S)[0])
                    diam = [contour_diameter(r) for r in rings if len(r) >= 3]
                    print(f"  Medis lumen {seg}: {len(rings)} rings ({how}), bounds {bounds(R)}; ring points to the "
                          f"nearest predicted surface vertex median {np.median(d):.2f}, 90th pct {np.percentile(d, 90):.2f} mm; "
                          f"Medis ring diameter median {np.median(diam):.2f} mm")
                print(f"  predicted lumen surface bounds {bounds(S)}")
        except Exception as ex:  # noqa: BLE001 - shown, the next participant goes on
            import traceback
            print(f"  stopped here: {type(ex).__name__}: {ex}")
            print("\n".join("    " + l for l in traceback.format_exc().splitlines()[-6:]))
        print()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=PRED_DIR)
    ap.add_argument("--medis", default=str(Path(hq.ROOT) / hq.MEDIS_DIR))
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--out", default=str(Path(__file__).resolve().with_suffix(".md")))
    args = ap.parse_args()
    buf = io.StringIO()
    stdout = sys.stdout
    sys.stdout = Tee(stdout, buf)
    try:
        probe(args)
    finally:
        sys.stdout = stdout
        Path(args.out).write_text("# Lumen prediction format (lumen_probe.py)\n\n```\n" + buf.getvalue() + "```\n")
        print(f"written to {args.out}")


if __name__ == "__main__":
    main()
