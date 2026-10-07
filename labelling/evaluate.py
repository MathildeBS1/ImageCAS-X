"""Evaluate a trained labeller on delivered or extracted test trees.

    python -m labelling.evaluate --run gnn3 --source delivered
    python -m labelling.evaluate --run gnn3 --source cas_net_pretrained_t3

Needs ``python -m labelling.data --source <source> --split test``. Everything is measured on
points, weighted by the centerline length each stands for, with and without tree decoding.
Points that match no delivered point (``SPURIOUS``) carry no true label: they are excluded from
accuracy and reported separately by what the model calls them. Writes
``RESULTS/labeller/<run>/eval_<source>/<id>.json`` per case and ``summary.json``.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict

import numpy as np
import torch

from bifurcation import graph, paths

from . import data, model
from .train import OUT

MAIN = {1, 2, 3, 9}  # LM, LAD, LCX, RCA


def _dominance(labels_mm: dict[int, float]) -> str:
    """R / L / Co from which PDA the tree carries (more than 10 mm of it)."""
    r, l = labels_mm.get(10, 0) > 10, labels_mm.get(12, 0) > 10
    return "Co" if r and l else "L" if l else "R"


def _f1(conf: dict[tuple[int, int], float]) -> dict:
    labels = sorted({t for t, _ in conf if t >= 0})
    out = {}
    for lab in labels:
        tp = conf.get((lab, lab), 0.0)
        fn = sum(v for (t, p), v in conf.items() if t == lab and p != lab)
        fp = sum(v for (t, p), v in conf.items() if p == lab and t != lab and t >= 0)
        prec, rec = tp / (tp + fp) if tp + fp else 0.0, tp / (tp + fn) if tp + fn else 0.0
        out[graph.artery_name(lab)] = {"f1": 2 * prec * rec / (prec + rec) if prec + rec else 0.0,
                                       "precision": prec, "recall": rec, "support_mm": tp + fn}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--source", default="delivered")
    ap.add_argument("--split", default="test", choices=["train", "val", "test"])
    args = ap.parse_args()
    ck = torch.load(OUT / args.run / "model.pt", weights_only=False)
    net = model.TreeGNN(ck["n_in"], ck["args"]["hidden"], ck["args"]["layers"])
    net.load_state_dict(ck["state_dict"])
    net.eval()
    out = OUT / args.run / f"eval_{args.source}"
    out.mkdir(parents=True, exist_ok=True)
    desc = paths.descriptors()

    conf = {"raw": defaultdict(float), "decoded": defaultdict(float)}
    spurious = defaultdict(float)
    per_case = defaultdict(dict)
    for case, side, segs in data.load(args.source, args.split):
        if not segs:
            per_case[case][side] = {"error": "empty tree"}
            continue
        g = data.featurize(segs, side)
        with torch.no_grad():
            x, par, _, _ = model.collate([g], ck["mean"], ck["std"])
            logp = torch.log_softmax(net(x, par)[side], 1).numpy()
        tr = ck["transitions"][side]
        preds = {"raw": logp.argmax(1), "decoded": model.viterbi(logp, g.parent, tr["T"], tr["root"])}
        cls = data.CLASSES[side]
        row = {}
        for mode, pred in preds.items():
            ok, tot = model.point_correct(g, pred)
            row[f"acc_{mode}"] = ok / tot if tot else None
            row[f"violation_{mode}"] = model.violation_rate(pred, g.parent, tr["T"])
            mm = defaultdict(float)
            for k, (lab, w) in enumerate(zip(g.lab, g.w)):
                p = cls[pred[k]]
                mm[p] += float(w.sum())
                for t in np.unique(lab):
                    v = float(w[lab == t].sum())
                    if t == data.SPURIOUS:
                        if mode == "decoded":
                            spurious[graph.artery_name(p)] += v
                    else:
                        conf[mode][(int(t), p)] += v
            row[f"labels_mm_{mode}"] = {graph.artery_name(k): round(v, 1) for k, v in mm.items()}
            row[f"_mm_{mode}"] = dict(mm)
        per_case[case][side] = row

    dom = {"raw": [], "decoded": []}
    for case, sides in per_case.items():
        for mode in dom:
            mm = defaultdict(float)
            for r in (sides[s] for s in ("left", "right") if s in sides):
                for k, v in r.pop(f"_mm_{mode}", {}).items():
                    mm[k] += v
            sides[f"dominance_{mode}"] = _dominance(mm)
            dom[mode].append(sides[f"dominance_{mode}"] == desc.loc[case, "Dominance"])
        sides["dominance_true"] = desc.loc[case, "Dominance"]
        (out / f"{case}.json").write_text(json.dumps(sides, indent=2) + "\n")

    summary = {"run": args.run, "source": args.source, "split": args.split, "checkpoint_epoch": ck["epoch"]}
    for mode, c in conf.items():
        tot = sum(c.values())
        f1 = _f1(c)
        main_tot = sum(v for (t, _), v in c.items() if t in MAIN)
        rows = [s[d] for s in per_case.values() for d in ("left", "right") if d in s and "error" not in s[d]]
        summary[mode] = {
            "point_accuracy": sum(v for (t, p), v in c.items() if t == p) / tot,
            "main_vessel_accuracy": sum(v for (t, p), v in c.items() if t == p and t in MAIN) / main_tot,
            "macro_f1": float(np.mean([v["f1"] for v in f1.values()])),
            "per_label": f1,
            "violation_rate_mean": float(np.mean([r[f"violation_{mode}"] for r in rows])),
            "dominance_accuracy": float(np.mean(dom[mode])),
            "confusion_mm": {f"{graph.artery_name(t)}->{graph.artery_name(p)}": round(v, 1) for (t, p), v in sorted(c.items())},
        }
    summary["spurious_mm_labelled_as"] = {k: round(v, 1) for k, v in spurious.items()}
    summary["n_failed"] = sum("error" in s[d] for s in per_case.values() for d in ("left", "right") if d in s)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    for mode in conf:
        s = summary[mode]
        print(f"{mode:8s} point acc {s['point_accuracy']:.3f}  main {s['main_vessel_accuracy']:.3f}  "
              f"macro F1 {s['macro_f1']:.3f}  violations {s['violation_rate_mean']:.3f}  dominance {s['dominance_accuracy']:.3f}")


if __name__ == "__main__":
    main()
