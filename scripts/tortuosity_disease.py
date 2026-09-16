#!/usr/bin/env python
"""Tortuosity panel (topology/tortuosity.py) against disease status: does any of it separate
ImageCAS-X's diseased cases from its healthy ones, and does the answer depend on which metric's
reproducibility (scripts/tortuosity_sensitivity.py) is trusted?

Reports, healthy vs. diseased (Mann-Whitney U, Benjamini-Hochberg FDR across every vessel x metric
test):
  1. every metric in the panel, per named vessel
  2. whether the significant metrics are an artefact of Image Quality, itself weakly associated
     with Disease: the same tests re-run within Image Quality == 4 only
  3. minimum detectable effect, at this cohort's size and 80% power, for the metrics that came
     back null -- so a null is reported as well powered or underpowered, not left unqualified

Usage:  python scripts/tortuosity_disease.py [--n N]
"""

from __future__ import annotations

import argparse
import json

import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower

from topology import paths, tortuosity

METRICS = ["distance_metric", "soam_per_mm", "curvature_mean", "curvature_max", "curvature_rms",
          "torsion_mean_abs", "non_planarity", "bends_over_45",
          "plane_d_max_mm", "plane_d_rms_mm", "plane_d_rms_norm",
          "plane_angle_mean_deg", "plane_angle_max_deg",
          "soam_window_max_per_mm", "curvature_rms_window_max"]

#: The metrics scripts/tortuosity_sensitivity.py found stable under a sigma 0-2mm sweep.
STABLE = ("distance_metric", "non_planarity", "plane_d_rms_norm", "plane_angle_mean_deg")


def _fdr(tests: list[dict]) -> None:
    ps = np.array([t["p"] for t in tests])
    order = np.argsort(ps)
    m = len(ps)
    q = np.empty(m)
    prev = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        i = m - rank + 1
        prev = min(prev, ps[idx] * m / i)
        q[idx] = prev
    for t, qv in zip(tests, q):
        t["q"] = float(qv)


def _extract(ids) -> list[dict]:
    desc = paths.descriptors()
    rows = []
    for cid in ids:
        try:
            vs = tortuosity.extract_case(cid)
        except Exception as exc:
            print(f"  case {cid} FAILED: {type(exc).__name__}: {exc}")
            continue
        disease = desc.loc[cid, "Disease"] if cid in desc.index else None
        disease = disease if isinstance(disease, str) else None
        iq = desc.loc[cid, "Image Quality"] if cid in desc.index else None
        for v in vs:
            row = {"case_id": cid, "name": v.name, "disease": disease, "image_quality": iq}
            row.update({m: getattr(v, m) for m in METRICS})
            rows.append(row)
    return rows


def _test(rows, metric, extra_filter=None):
    a = [r[metric] for r in rows if r["disease"] == "no" and np.isfinite(r[metric])
         and (extra_filter is None or extra_filter(r))]
    b = [r[metric] for r in rows if r["disease"] == "yes" and np.isfinite(r[metric])
         and (extra_filter is None or extra_filter(r))]
    a, b = np.array(a), np.array(b)
    if len(a) < 10 or len(b) < 10:
        return None
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {"n_h": len(a), "n_d": len(b), "med_h": float(np.median(a)), "med_d": float(np.median(b)),
            "sd_h": float(np.std(a)), "p": float(p)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0)
    args = ap.parse_args()

    ids = paths.usable_ids()[: args.n or None]
    print(f"=== 1/3 extracting tortuosity panel, {len(ids)} cases ===")
    rows = _extract(ids)
    rows = [r for r in rows if r["disease"] in ("yes", "no")]
    print(f"{len(rows)} vessel rows, {len({r['case_id'] for r in rows})} cases with a Disease label")

    print("\n=== 2/3 healthy vs. diseased, every vessel x metric (FDR across all tests) ===")
    tests = []
    for name in tortuosity.VESSEL_SIDES:
        sub = [r for r in rows if r["name"] == name]
        for metric in METRICS:
            result = _test(sub, metric)
            if result is None:
                continue
            result.update(vessel=name, metric=metric, stable=metric in STABLE)
            tests.append(result)
    _fdr(tests)
    for t in sorted(tests, key=lambda t: t["p"]):
        pct = 100 * (t["med_d"] - t["med_h"]) / t["med_h"] if t["med_h"] else float("nan")
        sig, tag = ("*" if t["q"] < 0.05 else " "), ("stable" if t["stable"] else "")
        print(f"  {t['vessel']:<4}{t['metric']:<24}{tag:<7} n_h={t['n_h']:>4} n_d={t['n_d']:>4}  "
              f"{t['med_h']:>9.4g} -> {t['med_d']:>9.4g}  ({pct:+6.1f}%)  p={t['p']:.3g}  q={t['q']:.3g}{sig}")
    n_sig = sum(1 for t in tests if t["q"] < 0.05)
    print(f"  {n_sig}/{len(tests)} survive FDR<0.05")

    print("\n=== 3/3 Image Quality confound: is Disease itself confounded, and does the "
          "significant curvature/SOAM effect survive holding quality fixed? ===")
    by_case = {r["case_id"]: r for r in rows}  # one row per case_id for the case-level IQ test
    iq_h = [r["image_quality"] for r in by_case.values() if r["disease"] == "no"]
    iq_d = [r["image_quality"] for r in by_case.values() if r["disease"] == "yes"]
    u, p_iq = stats.mannwhitneyu(iq_h, iq_d)
    print(f"  Image Quality, healthy vs. diseased: median {np.median(iq_h):.0f} vs "
          f"{np.median(iq_d):.0f}, p={p_iq:.3g}")
    sig_metrics = sorted({t["metric"] for t in tests if t["q"] < 0.05})
    best_quality = lambda r: r["image_quality"] == 4
    for name in tortuosity.VESSEL_SIDES:
        sub = [r for r in rows if r["name"] == name]
        for metric in sig_metrics:
            result = _test(sub, metric, extra_filter=best_quality)
            if result is None:
                continue
            pct = 100 * (result["med_d"] - result["med_h"]) / result["med_h"] if result["med_h"] else float("nan")
            print(f"  {name:<4}{metric:<24} IQ=4 only, n_h={result['n_h']:>4} n_d={result['n_d']:>4}  "
                  f"({pct:+6.1f}%)  p={result['p']:.3g}")

    print("\n=== minimum detectable effect for the stable metrics that came back null (80% power) ===")
    analysis = TTestIndPower()
    for t in tests:
        if t["q"] >= 0.05 and t["stable"] and t["med_h"]:
            mde = analysis.solve_power(effect_size=None, nobs1=t["n_h"],
                                       ratio=t["n_d"] / t["n_h"], alpha=0.05, power=0.8) * t["sd_h"]
            print(f"  {t['vessel']:<4}{t['metric']:<24} sd={t['sd_h']:.4g}  "
                  f"min. detectable effect={mde:.4g} ({100*mde/t['med_h']:+.1f}% of the healthy median)")

    out = paths.output_dir("tortuosity/disease")
    (out / "summary.json").write_text(json.dumps({"tests": tests}, indent=2) + "\n")
    print(f"\nWrote {out / 'summary.json'}")


if __name__ == "__main__":
    main()
