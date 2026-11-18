"""Show the file format of the in-house tracer centerlines, so tracer_io.py can be written from it.

    python CGPS_data/thesis_final/tracer_probe.py [--src TRACER_FOLDER] [--n 3]

For --n baseline participants that have a tracer pair and a Medis tree, prints per file
(left / right, plain / _ostium_pruned): the VTK header, points, cells by type, and every point and cell
data array (dtype, shape, number of distinct values, the first distinct values), then the bounding box of
the points next to that of the Medis tree and, where a BL volume is found under NIFTI/, of the volume in
voxel and in world (RAS and LPS) mm. Without a volume, the tracer and Medis bounds alone show whether the two
share a frame.
Participants are printed as 1, 2, 3; no study_id leaves the server. Read-only.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the shared modules in CGPS_data/
import centerline_qc as cq
import hoe10y_qc as hq

TRACER_DIR = "/data/kimbr/centerlines_for_mathilde"
MEDIS_TREES = Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"
SIDES = ("left", "right")
KINDS = ("", "_ostium_pruned")


def bounds(P):
    P = np.asarray(P, float)
    return " ".join(f"[{lo:8.1f}, {hi:8.1f}]" for lo, hi in zip(P.min(0), P.max(0)))


def describe_array(name, a):
    a = np.asarray(a)
    u = np.unique(a.reshape(len(a), -1), axis=0) if a.ndim > 1 else np.unique(a)
    first = ", ".join(str(np.round(v, 3).tolist()) for v in u[:8])
    return f"    {name}: dtype {a.dtype}, shape {a.shape}, {len(u)} distinct; first: {first}"


def show_file(path):
    data = path.read_bytes()
    print(f"  {path.name.split('.', 1)[1]}  ({len(data) / 1e3:.0f} kB)")
    print("    first line: " + data[:60].split(b"\n")[0].decode("latin-1", "replace"))
    try:
        v = cq.read_vtk_legacy(data)
    except Exception as ex:  # noqa: BLE001 - not legacy VTK: show the raw start instead
        print(f"    not read as legacy VTK ({type(ex).__name__}: {ex}); first 600 bytes:")
        print(data[:600].decode("latin-1", "replace"))
        return None
    P = v["points"]
    print(f"    {len(P)} points; bounds {bounds(P)}")
    print("    cells: " + (", ".join(f"{t} {len(c)} (lengths {min(map(len, c))}-{max(map(len, c))})"
                                     for t, c in v["cells"].items() if c) or "none"))
    step = np.linalg.norm(np.diff(P, axis=0), axis=1)
    print(f"    consecutive point spacing: median {np.median(step):.3f}, 95th pct {np.percentile(step, 95):.3f}")
    for kind in ("point_data", "cell_data", "field_data"):
        if v.get(kind):
            print(f"    {kind}:")
            for name, a in v[kind].items():
                print(describe_array(name, a))
    return P


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=TRACER_DIR)
    ap.add_argument("--n", type=int, default=3)
    args = ap.parse_args()
    src = Path(args.src)
    files = sorted(src.glob("BL_*.vtk"))
    print(f"{len(files)} BL files, {len(list(src.glob('FU_*.vtk')))} FU files in {src}")
    names = {p.name.split(".", 1)[1] for p in files}
    print("BL file kinds: " + ", ".join(sorted(names)))
    ids = sorted({hq.id_from_name(p.name.split(".", 1)[0]) for p in files}, key=int)
    print(f"{len(ids)} BL participants with a tracer file")

    medis = {hq.id_from_name(p.name): p for p in MEDIS_TREES.rglob("*.vtk")}
    niftis = {}
    for p in (Path(hq.ROOT) / hq.NIFTI_DIR).rglob("*.nii*") if (Path(hq.ROOT) / hq.NIFTI_DIR).is_dir() else []:
        if hq.visit_from_path(p.relative_to(hq.ROOT)) == "BL":
            niftis[hq.id_from_name(p.name)] = p
    both = [i for i in ids if i in medis]
    pruned = {s: {hq.id_from_name(p.name.split(".", 1)[0]) for p in src.glob(f"BL_*.coronary_{s}_centerline_ostium_pruned.vtk")}
              for s in SIDES}
    print("\nBL trees, Medis against the tracer (participants):")
    print(f"  Medis trees                          {len(medis)}")
    print(f"  tracer, any file                     {len(ids)}")
    print(f"  tracer, pruned left and right        {len(pruned['left'] & pruned['right'])}")
    print(f"  tracer, pruned left only / right only {len(pruned['left'] - pruned['right'])} / "
          f"{len(pruned['right'] - pruned['left'])}")
    print(f"  in both Medis and tracer             {len(both)}")
    print(f"    with pruned left and right         {len([i for i in both if i in pruned['left'] & pruned['right']])}")
    print(f"  Medis only (no tracer file)          {len(set(medis) - set(ids))}")
    print(f"  tracer only (no Medis tree)          {len(set(ids) - set(medis))}")
    print(f"  in both, with a BL NIfTI             {sum(i in niftis for i in both)}\n")

    order = [i for i in both if i in niftis] + [i for i in both if i not in niftis]
    for k, pid in enumerate(order[: args.n], 1):
        print(f"=== participant {k}")
        for side in SIDES:
            for kind in KINDS:
                p = src / f"BL_{pid}.coronary_{side}_centerline{kind}.vtk"
                if p.exists():
                    show_file(p)
                else:
                    print(f"  {side}{kind}: missing")
        M = np.concatenate([pts for pts, _ in hq.tree_points(medis[pid])])
        print(f"  Medis tree: {len(M)} points; bounds {bounds(M)}")
        if pid not in niftis:
            print("  volume: no BL NIfTI found\n")
            continue
        import nibabel as nib
        img = nib.load(str(niftis[pid]))
        corners = np.array([[i, j, kk] for i in (0, img.shape[0] - 1) for j in (0, img.shape[1] - 1)
                            for kk in (0, img.shape[2] - 1)], float)
        ras = corners @ img.affine[:3, :3].T + img.affine[:3, 3]
        print(f"  volume: shape {img.shape[:3]}, zooms {tuple(round(z, 3) for z in img.header.get_zooms()[:3])}, "
              f"axcodes {''.join(nib.aff2axcodes(img.affine))}")
        print(f"    voxel bounds {bounds(corners)}")
        print(f"    RAS mm bounds {bounds(ras)}")
        print(f"    LPS mm bounds {bounds(ras * [-1, -1, 1])}\n")


if __name__ == "__main__":
    main()
