"""Medis against itself: the landmark rule run on the Medis trunks, against the Medis segment labels.

    python CGPS_data/medis_landmark_check.py [--src TREE_FOLDER] [--out MD]

The centerline is the same on both sides, so any disagreement is boundary placement only. For every
trunk with Medis p/m/d labels, split_trunks.split() gives the Medis boundaries and the landmark
boundaries, with branch labels and label-free (side-branch length only, as for the in-house tracer).
Reported per artery and rule:
1. the share of the trunk length (up to the shorter of the two ends) given the same segment label;
2. the error of each boundary, landmark - Medis, in mm along the trunk.
Where Medis has one LCx label for mcx + dcx, its m/d boundary is itself a branch rule (split_trunks),
so that boundary is left out and mcx + dcx count as one segment in the share.
The trees are split into half A (for tuning LAD_MD_FRAC and the acute-margin rule) and half B (for
reporting) by a checksum of the file name. The RCA is run with both acute-margin rules (ACUTE), and
the Medis boundaries are also given as fractions (LAD m/d from D1 to the end, RCA m/d of the crux).
Aggregates only (counts 1-4 hidden); writes medis_landmark_check.md.
"""

import argparse
import zlib
from pathlib import Path

import pandas as pd

import hoe10y_qc as hq
from cgps_stats import OUT_DIR, describe
import split_trunks as st
from split_trunks import graph, split, table

RULES = {"landmark": "with branch labels", "label_free": "label-free"}
st_acute = st.ACUTE  # the setting in split_trunks; the other rule is run for comparison
ACUTES = (st_acute, *[a for a in ("turn", "chord") if a != st_acute])
KEYS = ["half", "artery", "rule", "acute"]


def share(a, b, merge_md=False):
    """Share of the common length that two (pm, md, end) splits give the same segment."""
    L = min(a[2], b[2])
    if L <= 0:
        return None
    seg = lambda c: [(0, c[0]), (c[0], L)] if merge_md else [(0, c[0]), (c[0], c[1]), (c[1], L)]
    same = sum(max(0.0, min(h1, h2, L) - max(l1, l2)) for (l1, h1), (l2, h2) in zip(seg(a), seg(b)))
    return same / L


def collect(files):
    rows = []
    for f in files:
        half = "A" if zlib.crc32(f.name.encode()) % 2 == 0 else "B"
        try:
            tree = graph(hq.tree_points(f))
        except Exception:  # noqa: BLE001 - tree left out
            continue
        for acute in ACUTES:
            st.ACUTE, info = acute, {}
            try:
                res = split(*tree, info=info)
            except Exception:  # noqa: BLE001 - tree left out
                continue
            for a, d in info.items():
                if d.get("landmark") is None or a not in res or (a != "RCA" and acute != st_acute):
                    continue  # no Medis p/m/d labels, or LAD/CX already done (ACUTE is RCA only)
                medis, merge = res[a][:3], "mcx/dcx" in res[a][3]
                for how in RULES:
                    lm = d[how]
                    frac = ((medis[1] - lm[0]) / (lm[2] - lm[0]) if a == "LAD" and lm[2] > lm[0]
                            else medis[1] / medis[2] if a == "RCA" and medis[2] > 0 else None)
                    rows.append({"half": half, "artery": a, "rule": how, "acute": acute if a == "RCA" else "",
                                 "share": share(medis, lm, merge), "pm": lm[0] - medis[0],
                                 "md": None if merge else lm[1] - medis[1],
                                 "crux": lm[2] - medis[2] if a == "RCA" else None, "medis_frac": frac})
    st.ACUTE = st_acute
    return pd.DataFrame(rows)


def report(df, n_files):
    q = lambda d, k: "" if d.get(k) is None else f"{d[k]:.2f}" if k.startswith("s") else f"{d[k]:.1f}"
    L = ["# Landmark rule vs Medis labels on the Medis trunks (medis_landmark_check.py)\n",
         f"Aggregates only; counts 1-4 shown as <5. {n_files} tree files.\n"]
    if not len(df):
        return "\n".join(L + ["No trunk with Medis p/m/d labels.\n"])
    rows = []
    for (h, a, how, ac), g in df.groupby(KEYS):
        d = describe(g["share"])
        rows.append((h, a, RULES[how], ac, d["n"], q(d, "median"), f"{q(d, 'p25')} to {q(d, 'p75')}"))
    L += ["## Share of trunk length with the same segment label\n",
          "Half A is for tuning, half B for reporting; acute = RCA acute-margin rule.\n",
          table(["half", "artery", "rule", "acute", "trunks", "median", "p25 to p75"], rows)]
    rows = []
    for (h, a, how, ac), g in df.groupby(KEYS):
        for b in ("pm", "md", "crux") if a == "RCA" else ("pm", "md"):
            d, da = describe(g[b]), describe(g[b].abs())
            rows.append((h, a, {"pm": "p/m", "md": "m/d", "crux": "crux (end of d)"}[b], RULES[how], ac, d["n"],
                         q(d, "median"), f"{q(d, 'p25')} to {q(d, 'p75')}", q(da, "median")))
    L += ["## Boundary error, landmark - Medis (mm along the trunk)\n",
          "LAD m/d and RCA p/m sit at a fraction of a length, so they also move with where the trunk ends.\n",
          table(["half", "artery", "boundary", "rule", "acute", "trunks", "median", "p25 to p75", "median abs"], rows)]
    rows = []
    sub = df[(df["half"] == "A") & (df["rule"] == "landmark") & (df["acute"].isin(["", st_acute]))]
    for a, name in (("LAD", "Medis m/d as fraction from D1 to the LAD end (for LAD_MD_FRAC)"),
                    ("RCA", "Medis m/d (acute margin) as fraction of the Medis crux")):
        d = describe(sub.loc[sub["artery"] == a, "medis_frac"])
        rows.append((name, d["n"], f"{d['median']:.2f}" if d.get("median") is not None else "",
                     f"{q(d, 'p25')} to {q(d, 'p75')}"))
    L += ["## Medis boundaries as fractions (half A)\n",
          table(["quantity", "trunks", "median", "p25 to p75"], rows)]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path(hq.ROOT) / "Medis" / "Analysis_Processed" / "centerline_tree"))
    ap.add_argument("--out", default=str(Path(OUT_DIR) / "medis_landmark_check.md"))
    args = ap.parse_args()
    files = sorted(Path(args.src).rglob("*.vtk"))
    hq.read_label_codes((f, f) for f in files)  # names for codes a file leaves unnamed, as in split_trunks
    df = collect(files)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(report(df, len(files)), encoding="utf-8")
    print(f"{len(files)} trees -> {args.out}")


if __name__ == "__main__":
    main()
