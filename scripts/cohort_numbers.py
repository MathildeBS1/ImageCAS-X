#!/usr/bin/env python
"""Every cohort number quoted in the clinical background chapter, in one place.

The thesis states figures from this cohort beside published ones, so each has to be
re-derivable from the code rather than copied out of a notebook. This script prints
all of them and writes them as JSON with the code version attached, so a number in
the text can always be traced to the commit that produced it.

``scripts/survey_topology.py`` validates the trees; this one describes them.

    python scripts/cohort_numbers.py            # print, and write JSON to the derived tree
"""

from __future__ import annotations

import argparse
import collections
import json

import numpy as np

from topology import graph, paths

#: Reported in the order the chapter uses them.
LEFT_ARTERIES = ["LM", "LAD", "LCX", "D1", "D2", "OM1", "OM2", "IM"]
POSTERIOR = ["R-PDA", "R-PLA", "L-PDA", "L-PLA"]


def collect() -> list[dict]:
    """One row per case: which arteries are labelled, and the left-tree topology."""
    desc = paths.descriptors()
    rows = []
    for cid in paths.usable_ids():
        left = graph.load_tree(cid, "left")
        right = graph.load_tree(cid, "right")
        names = {s.name for s in left.segments} | {s.name for s in right.segments}
        ostia = [n for n in left.nodes.values() if n.kind == graph.OSTIUM]

        # Where the ramus intermedius leaves: one three-way node, or two branch points
        # a short distance apart. The distinction is a decision the feature code has to
        # make, so it is measured rather than assumed.
        origin_spread = None
        if "IM" in names:
            depth: dict[int, float] = {}
            start: dict[int, float] = {}
            for seg in left.walk():
                start[seg.index] = 0.0 if seg.parent is None else depth[seg.parent]
                depth[seg.index] = start[seg.index] + seg.length
            origins = []
            for nm in ("IM", "LAD", "LCX"):
                segs = [s for s in left.segments if s.name == nm]
                if segs:
                    origins.append(start[min(segs, key=lambda s: s.index).index])
            if len(origins) == 3:
                origin_spread = max(origins) - min(origins)

        rows.append({
            "case_id": cid,
            "dominance": desc.loc[cid, "Dominance"],
            "quality": int(desc.loc[cid, "Image Quality"]),
            "arteries": names,
            "n_ostia_left": len(ostia),
            "ostium_separation_mm": (
                float(np.linalg.norm(ostia[0].position - ostia[1].position))
                if len(ostia) == 2 else None
            ),
            "lm_length_mm": sum(s.length for s in left.segments if s.name == "LM"),
            "im_origin_spread_mm": origin_spread,
        })
    return rows


def pct(k: int, n: int) -> float:
    return round(100.0 * k / n, 1) if n else float("nan")


def stats(values) -> dict:
    a = np.asarray([v for v in values if v is not None], dtype=float)
    return {
        "n": int(a.size), "median": round(float(np.median(a)), 1),
        "q1": round(float(np.quantile(a, 0.25)), 1), "q3": round(float(np.quantile(a, 0.75)), 1),
        "min": round(float(a.min()), 1), "max": round(float(a.max()), 1),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="output directory (default: derived tree)")
    args = ap.parse_args()

    rows = collect()
    n = len(rows)
    doms = ["R", "L", "Co"]
    by_dom = {d: [r for r in rows if r["dominance"] == d] for d in doms}

    prevalence = {
        a: {"all": pct(sum(a in r["arteries"] for r in rows), n),
            **{d: pct(sum(a in r["arteries"] for r in g), len(g)) for d, g in by_dom.items()}}
        for a in LEFT_ARTERIES + POSTERIOR
    }
    no_lm = [r for r in rows if "LM" not in r["arteries"]]
    two_ostia = [r for r in rows if r["n_ostia_left"] == 2]
    im = [r for r in rows if "IM" in r["arteries"]]
    spread = [r["im_origin_spread_mm"] for r in im if r["im_origin_spread_mm"] is not None]
    single_node = [s for s in spread if s < 1e-9]

    out = {
        "code_version": paths.code_version(),
        "n_cases": n,
        "dominance_counts": {d: len(g) for d, g in by_dom.items()},
        "dominance_pct": {d: pct(len(g), n) for d, g in by_dom.items()},
        "quality_counts": dict(sorted(collections.Counter(r["quality"] for r in rows).items())),
        "prevalence_pct": prevalence,
        "left_main": {
            "present": n - len(no_lm),
            "absent": len(no_lm),
            "absent_pct": pct(len(no_lm), n),
            "absent_ids": sorted(r["case_id"] for r in no_lm),
            "trunk_length_mm": stats([r["lm_length_mm"] for r in rows if "LM" in r["arteries"]]),
        },
        "two_ostia_left": {
            "n": len(two_ostia),
            "ids": sorted(r["case_id"] for r in two_ostia),
            # Two of the 13 (84, 272) are fragmented sides with one true ostium, so the
            # separation is only anatomy over the 11 that also have no LM label.
            "same_as_absent_lm": {r["case_id"] for r in two_ostia} == {r["case_id"] for r in no_lm},
            "separation_mm_absent_lm": stats(
                [r["ostium_separation_mm"] for r in no_lm if r["ostium_separation_mm"] is not None]
            ),
        },
        "ramus_intermedius": {
            "n": len(im),
            "pct": pct(len(im), n),
            "by_dominance_pct": {d: pct(sum("IM" in r["arteries"] for r in g), len(g))
                                 for d, g in by_dom.items()},
            "single_node_trifurcation": len(single_node),
            "single_node_pct": pct(len(single_node), len(spread)),
            "origin_spread_mm_when_not_single_node": stats([s for s in spread if s >= 1e-9]),
        },
    }

    print(f"n = {n} usable cases  (code {out['code_version']})\n")
    print("Dominance:", ", ".join(f"{d} {len(g)} ({pct(len(g), n)}%)" for d, g in by_dom.items()))
    print("\nPrevalence of each artery label (%):")
    print(f"  {'':<8}{'all':>7}{'R':>7}{'L':>7}{'Co':>7}")
    for a in LEFT_ARTERIES + POSTERIOR:
        p = prevalence[a]
        print(f"  {a:<8}{p['all']:>7}{p['R']:>7}{p['L']:>7}{p['Co']:>7}")

    lm = out["left_main"]
    print(f"\nLeft main: present in {lm['present']}, absent in {lm['absent']} ({lm['absent_pct']}%)")
    t = lm["trunk_length_mm"]
    print(f"  trunk length mm: median {t['median']} (IQR {t['q1']}-{t['q3']}, range {t['min']}-{t['max']}, n={t['n']})")
    s = out["two_ostia_left"]["separation_mm_absent_lm"]
    print(f"  two left ostia in {out['two_ostia_left']['n']} sides; same set as no-LM: "
          f"{out['two_ostia_left']['same_as_absent_lm']}")
    print(f"  ostium separation mm (the {s['n']} absent-LM sides): median {s['median']} "
          f"(range {s['min']}-{s['max']})")

    r = out["ramus_intermedius"]
    print(f"\nRamus intermedius: {r['n']} cases ({r['pct']}%), by dominance "
          + ", ".join(f"{d} {v}%" for d, v in r["by_dominance_pct"].items()))
    sp = r["origin_spread_mm_when_not_single_node"]
    print(f"  leaves at one three-way node in {r['single_node_trifurcation']} ({r['single_node_pct']}%);")
    print(f"  otherwise IM/LAD/LCX origins span median {sp['median']} mm "
          f"(IQR {sp['q1']}-{sp['q3']}, max {sp['max']})")

    out_dir = paths.output_dir("cohort_numbers") if args.out is None else __import__("pathlib").Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "cohort_numbers.json"
    path.write_text(json.dumps(out, indent=2, default=str) + "\n")
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
