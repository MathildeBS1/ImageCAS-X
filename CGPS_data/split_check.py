"""Does the trunk split (split_trunks.py) put each segment where Medis and the visual analysis have it?

    python CGPS_data/split_check.py [--medis MEDIS_FOLDER] [--out MD]

Medis has a contour set (centerline, lumen, outer wall) for each diseased BL segment, named by
segment (BL_996_pLAD_lumen.vtk). Each contour is projected onto the split trunk of its artery
(nearest trunk point; off the trunk if the median distance is > 2 mm), giving its extent in mm along
the trunk (5th to 95th percentile of the projected lumen-ring centres; the contour's centerline file
covers the whole vessel and is not used for the extent).

1. Contour vs split: which split segment holds most of each contour, the share of the contour inside
   the segment of the same name, and how far the contour ends lie from the split boundaries, by
   boundary source (Medis labels / landmark rule). Medis 'LCx' contours (cx) cover mcx + dcx.
2. Visual analysis: per tree and trunk segment, the BL visual grade against a Medis contour with the
   segment's name, and against a contour the split puts in the segment. If the split matches the
   visual read, contours by location agree with the visual plaque at least as well as by name.
3. The BL ct_cag_<segment>_medis_finished / _medis_egnet columns against contours by name.
Aggregates only (counts 1-4 hidden); writes split_check.md.
"""
import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import centerline_qc as cq
import hoe10y_qc as hq
from cgps_stats import OUT_DIR, count, describe, pct, suppress, yes
from split_trunks import ARTERY_OF, NAMES, graph, split, table

PLAQUE = ("minimal", "mild", "moderate", "severe", "occlusion")
OFF_TRUNK = 2.0  # mm: median contour-to-trunk distance above this = contour is not on the trunk
COVERS = {**{s: (s,) for segs in NAMES.values() for s in segs}, "cx": ("mcx", "dcx"),
          "lad": NAMES["LAD"], "rca": NAMES["RCA"]}  # contour name -> split segments it stands for
ORDER = [s for segs in NAMES.values() for s in segs]


def contour_files(medis):
    """(id, segment) -> {centerline/lumen/outer: path} for the BL trunk contours."""
    out = defaultdict(dict)
    for p in Path(medis).rglob("*.vtk"):
        m = hq.CONTOUR_RE.match(p.name)
        if m and m["visit"].upper() == "BL":
            out[(hq.norm_id(m["id"]), hq.seg_key(m["seg"]))][m["kind"].lower()] = p
    return out


def contour_points(files):
    """Centres of the lumen (else outer-wall) rings: the stretch Medis contoured. The contour's own
    centerline file runs along the whole vessel, so it is used only to group points into rings."""
    cl = cq.read_vtk_legacy(files["centerline"].read_bytes())["points"] if "centerline" in files else None
    kind = "lumen" if "lumen" in files else "outer" if "outer" in files else None
    if kind is None:
        raise ValueError("no ring file")
    rings, _ = hq.read_rings(files[kind], cl)
    return np.array([r.mean(0) for r in rings if len(r) >= 3])


def visual(bl, pid, seg):
    """BL visual class of a segment: plaque / none / unevaluable / no read."""
    col = f"ct_cag_{seg}_stenosis"
    if pid not in bl.index or col not in bl:
        return "no read"
    g = hq.grade_of(bl.at[pid, col])
    return "plaque" if g in PLAQUE else g if g in ("none", "unevaluable") else "no read"


def build(trees, contours, bl):
    cons, segs = [], []
    by_id = defaultdict(dict)
    for (pid, name), files in contours.items():
        by_id[pid][name] = files
    for f in trees:
        pid = hq.id_from_name(f.name)
        info = {}
        try:
            res = split(*graph(hq.tree_points(f)), info=info)
        except Exception:  # noqa: BLE001 - counted as no split
            res = {}
        bounds = {}
        for a, (pm, md, end, _, Y, s) in res.items():
            for seg, lo, hi in zip(NAMES[a], (0, pm, md), (pm, md, end)):
                bounds[seg] = (lo, hi, info[a]["source"])
        located = defaultdict(bool)
        for name, files in by_id.get(pid, {}).items():
            a = ARTERY_OF.get(name, "").upper()
            row = {"id": pid, "name": name, "artery": a or "side branch"}
            if not a:
                cons.append(row | {"status": "side branch"})
                continue
            if a not in res:
                cons.append(row | {"status": "artery not split"})
                continue
            try:
                P = contour_points(files)
            except Exception:  # noqa: BLE001 - counted
                cons.append(row | {"status": "unreadable"})
                continue
            Y, s = res[a][4], res[a][5]
            d, j = cq.nearest(P, Y)
            if len(P) < 2 or np.median(d) > OFF_TRUNK:
                cons.append(row | {"status": "off trunk"})
                continue
            lo, hi = np.percentile(s[np.ravel(j)], [5, 95])
            overlap = {g: max(0.0, min(hi, b[1]) - max(lo, b[0])) for g, b in bounds.items() if g in NAMES[a]}
            assigned = max(overlap, key=overlap.get)
            named = COVERS.get(name, ())
            row |= {"status": "on trunk", "assigned": assigned, "length": hi - lo,
                    "source": info[a]["source"],
                    "frac_named": sum(overlap[g] for g in named if g in overlap) / max(hi - lo, 1e-6),
                    "visual_named": "plaque" if any(visual(bl, pid, g) == "plaque" for g in named) else visual(bl, pid, named[0]) if named else "",
                    "visual_assigned": visual(bl, pid, assigned)}
            if name in bounds:  # boundary offsets only for p/m/d names (not cx / lad / rca)
                row |= {"start_off": lo - bounds[name][0], "end_off": hi - bounds[name][1]}
            located[assigned] = True
            cons.append(row)
        names = by_id.get(pid, {})
        for seg in ORDER:
            if seg in bounds and bounds[seg][1] - bounds[seg][0] >= 1.0:
                segs.append({"id": pid, "segment": seg, "visual": visual(bl, pid, seg),
                             "by_name": any(seg in COVERS.get(n, ()) for n in names),
                             "by_location": located[seg], "source": bounds[seg][2],
                             **{k: yes(pd.Series([bl.at[pid, f"ct_cag_{seg}_{k}"]])).iloc[0]
                                if pid in bl.index and f"ct_cag_{seg}_{k}" in bl else np.nan
                                for k in ("medis_finished", "medis_egnet")}})
    return pd.DataFrame(cons), pd.DataFrame(segs)


def crosstab(rows, cols, row_order=None, col_order=None):
    t = pd.crosstab(rows, cols)
    if row_order:
        t = t.reindex([r for r in row_order if r in t.index])
    if col_order:
        t = t.reindex(columns=col_order, fill_value=0)
    return t


def agreement(seg, col):
    """Of visual-plaque segments: share with a contour; of segments with a contour: share visual plaque."""
    ev = seg[seg["visual"].isin(["plaque", "none"])]
    vp, c = ev["visual"] == "plaque", ev[col]
    show = lambda v: "" if v is None else v
    return (show(pct((vp & c).sum(), vp.sum())), count(vp.sum()), show(pct((vp & c).sum(), c.sum())), count(c.sum()))


def report(cons, seg, n_trees, n_contours):
    q = lambda d, k: "" if d.get(k) is None else f"{d[k]:.1f}"
    iqr = lambda d: f"{q(d, 'p25')} to {q(d, 'p75')}" if d.get("p25") is not None else ""
    L = ["# Trunk split vs Medis contours and the visual analysis (split_check.py)\n",
         "Aggregates only; counts 1-4 shown as <5, percentages hidden where they would reveal them.\n",
         f"Trees: {count(n_trees)}; BL Medis contour sets: {count(n_contours)}.\n"]
    if not len(cons):
        return "\n".join(L + ["_No contours matched a tree._\n"])
    st = cons["status"].value_counts()
    L += ["## Contours\n", table(["status", "contours"], [(k, count(v)) for k, v in st.items()])]
    on = cons[cons["status"] == "on trunk"]
    if len(on):
        names = [n for n in (*ORDER, "lad", "cx", "rca") if n in set(on["name"])]
        t = crosstab(on["name"], on["assigned"], names, ORDER)
        t = t.loc[:, (t > 0).any()]
        L += ["## 1. Which split segment holds most of each contour\n",
              "Rows: the Medis contour's segment name; columns: the split segment with the largest overlap. "
              "A good split puts the counts on the diagonal (cx = Medis LCx, expected in mcx or dcx).\n",
              table(["contour", *t.columns], [(r, *v) for r, v in zip(t.index, suppress(t.to_numpy()))])]
        rows = []
        for (name, src), g in on.groupby(["name", "source"]):
            d, a, b = describe(g["frac_named"] * 100), describe(g.get("start_off", pd.Series(dtype=float))), \
                describe(g.get("end_off", pd.Series(dtype=float)))
            ln = describe(g["length"])
            rows.append((name, src, d["n"], q(ln, "median"), q(d, "median"), q(a, "median"), iqr(a), q(b, "median"), iqr(b)))
        rows.sort(key=lambda r: ((ORDER + ["lad", "cx", "rca"]).index(r[0]) if r[0] in ORDER + ["lad", "cx", "rca"] else 99, r[1]))
        L += ["Share of each contour inside the split segment(s) of its name, and the contour ends minus the "
              "split boundaries (mm; negative = contour starts / ends before the split boundary). Medis "
              "contours may cover only the diseased part of a segment, so the ends need not reach the "
              "boundaries; a consistent shift in one direction points at the split.\n",
              table(["contour", "split from", "contours", "median length (mm)", "median % inside", "start offset median", "p25 to p75",
                     "end offset median", "p25 to p75"], rows)]
        t = crosstab(on["visual_named"], on["visual_assigned"], ["plaque", "none", "unevaluable", "no read"],
                     ["plaque", "none", "unevaluable", "no read"])
        L += ["Visual BL grade of the segment the contour is named after (rows) and of the split segment that holds "
              "it (columns). Medis contours are drawn on diseased segments, so both should mostly be plaque.\n",
              table(["named \\ split", *t.columns], [(r, *v) for r, v in zip(t.index, suppress(t.to_numpy()))])]
    if len(seg):
        L += ["## 2. Split segments vs the visual analysis\n",
              "One row per tree and split trunk segment. A contour by name = a Medis contour named after the "
              "segment (a Medis LCx contour counts for both mcx and dcx); by location = a contour the split puts mostly "
              "in this segment.\n"]
        for col, title in (("by_name", "Medis contour by name"), ("by_location", "Medis contour by location")):
            t = crosstab(seg["visual"], seg[col].map({True: "contour", False: "no contour"}),
                         ["plaque", "none", "unevaluable", "no read"], ["contour", "no contour"])
            L += [f"{title}:\n", table(["visual BL", *t.columns], [(r, *v) for r, v in zip(t.index, suppress(t.to_numpy()))])]
        rows = [(title, *agreement(seg, col)) for col, title in (("by_name", "by name"), ("by_location", "by location"))]
        rows += [(f"by location, split from {s}", *agreement(seg[seg["source"] == s], "by_location"))
                 for s in ("medis_label", "landmark", "fraction") if (seg["source"] == s).any()]
        L += ["Agreement (visually evaluable segments only):\n",
              table(["contour", "% of visual plaque with a contour", "visual plaque", "% of contours with visual plaque",
                     "contours"], rows),
              "Per segment, by location:\n",
              table(["segment", "% of visual plaque with a contour", "visual plaque", "% of contours with visual plaque",
                     "contours"], [(s, *agreement(seg[seg["segment"] == s], "by_location")) for s in ORDER
                                   if (seg["segment"] == s).any()])]
        rows = []
        for k in ("medis_finished", "medis_egnet"):
            if seg[k].notna().any():
                t = crosstab(seg[k].map({1.0: "yes", 0.0: "no"}).fillna("empty"),
                             seg["by_name"].map({True: "contour", False: "no contour"}), ["yes", "no", "empty"],
                             ["contour", "no contour"])
                rows.append(f"`{k}`:\n")
                rows.append(table([k, *t.columns], [(r, *v) for r, v in zip(t.index, suppress(t.to_numpy()))]))
        if rows:
            L += ["## 3. Visual-analysis Medis status vs contours by name\n",
                  "The BL sheet fills these columns only for segments with plaque (empty otherwise).\n", *rows]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--medis", default=str(Path(hq.ROOT) / hq.MEDIS_DIR))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "split_check.md"))
    args = ap.parse_args()
    trees = sorted((Path(args.medis) / "Analysis_Processed" / "centerline_tree").rglob("*.vtk"))
    hq.read_label_codes((f, f) for f in trees)  # names for codes a file leaves unnamed
    contours = contour_files(args.medis)
    bl = hq.load_sheets(hq.ROOT)["BL"]
    bl = bl.assign(id=bl["study_id"].map(hq.norm_id)).drop_duplicates("id").set_index("id")
    cons, seg = build(trees, contours, bl)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(report(cons, seg, len(trees), len(contours)), encoding="utf-8")
    print(f"{len(trees)} trees, {len(contours)} BL contour sets -> {args.out}")


if __name__ == "__main__":
    main()
