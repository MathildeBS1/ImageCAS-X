"""What is inside a Medis centerline tree file? Prints array names and segment labels only (no IDs, no coordinates).

    python investigate.py [TREE_FOLDER] [N_FILES]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # find centerline_qc.py next to this file
SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "/data/kimbr/HØ_10Y/Medis/Analysis_Processed/centerline_tree")
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3

files = sorted(SRC.rglob("*.vtk"))
print(f"{len(files)} .vtk files under {SRC}")
for k, f in enumerate(files[:N], 1):
    raw = f.read_bytes()
    print(f"\n=== file {k} of {len(files)} ({len(raw) / 1e3:.0f} kB) ===")
    # 1. the readable text in the file: header, keywords, array names, segment names
    words = [w.decode("ascii") for w in re.findall(rb"[ -~]{4,}", raw)]
    print("header:", words[:3])
    print("keywords and arrays:", [w for w in words if re.match(r"^(DATASET|POINTS|LINES|POLYGONS|VERTICES|CELL_DATA|"
                                                               r"POINT_DATA|FIELD|SCALARS|LOOKUP_TABLE|VECTORS)\b|.*\b(int|float|double|string|vtkIdType)\b", w)][:40])
    print("segment names:", [w for w in words if re.match(r"^\d+:\S", w)][:40])
    # 2. the same file through the project's parser: one label per point
    try:
        import centerline_qc as cq
        polys, meta = cq.parse_member(f.name, raw)
        print("parser meta:", {key: v for key, v in meta.items() if key != "source"})
        labels = [str(lab) for p in polys for lab in p.labels]
        counts = {lab: labels.count(lab) for lab in sorted(set(labels))}
        print(f"{len(polys)} polylines, {len(labels)} points; points per label:", counts)
    except Exception as ex:  # noqa: BLE001 - show why, the text above still answers most of it
        print(f"centerline_qc not usable: {type(ex).__name__}: {ex}")
