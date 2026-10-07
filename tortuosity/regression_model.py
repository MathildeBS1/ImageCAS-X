"""Logistic regression of a yes/no scan outcome on one vessel's features, plus optional covariates.

    python -m tortuosity.regression_model --vessel LAD --outcome Disease        # fit on train, report val
    python -m tortuosity.regression_model --features T_5 T_8 length_mm          # any columns of the vessel CSVs
    python -m tortuosity.regression_model --covariates Age Sex                  # any columns of the descriptor sheets
    python -m tortuosity.regression_model --test                                # final run only: also reports test

Two kinds of model term, both unlimited in number:

--features are per-vessel columns of the CSVs written by `tortuosity.score` (default T_5 and
length_mm). Add one by adding a line to score.FEATURES and rescoring all three splits.
--covariates are per-scan columns of the sheets listed in paths.DESCRIPTORS (numbers used as
they are, text such as Sex split into 0/1 columns). Add one by adding a column to a sheet, or
a sheet to that list.

--vessel is LAD, LCX or RCA (default all three); --outcome is a yes/no descriptor column
(default Disease). The outcome is one value per scan, so each model asks how much that vessel's
features say about the scan. The run directory is named after the outcome plus every covariate
and every feature beyond the default pair, so distinct models never overwrite each other:
<RESULTS>/tortuosity_<outcome>[_<extras>]/<vessel>_{summary.txt,predictions.csv}.
"""
import argparse
import os
from functools import reduce

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from . import paths

BASE_FEATURES = ["T_5", "length_mm"]
SEED = 42


def descriptors():
    """The sheets of paths.DESCRIPTORS merged on case, one row per scan."""
    read = lambda p: (pd.read_excel if p.endswith((".xlsx", ".xls")) else pd.read_csv)(p).rename(columns={"Scan ID": "case"})
    return reduce(lambda a, b: a.merge(b, on="case", how="left"), map(read, paths.DESCRIPTORS))


def load(vessel, outcome, features, covariates):
    df = pd.concat([pd.read_csv(f"{paths.SCORES}/{s}_vessels.csv").assign(split=s) for s in ("train", "val", "test")])
    d = descriptors()[["case", outcome] + covariates]
    df = df[df.vessel == vessel].merge(d, on="case").dropna(subset=features + [outcome] + covariates)
    df["y"] = df[outcome].astype(str).str.lower().isin(["yes", "1", "true"]).astype(int)  # positive class
    text = [c for c in covariates if not pd.api.types.is_numeric_dtype(df[c])]
    dummies = pd.get_dummies(df[text], drop_first=True, dtype=float) if text else pd.DataFrame(index=df.index)  # e.g. Sex -> Sex_M
    df = df.join(dummies).reset_index(drop=True)
    return df, features + [c for c in covariates if c not in text] + list(dummies.columns)


def auc_ci(y, p, n=2000):
    rng = np.random.default_rng(SEED)
    b = [roc_auc_score(y[i], p[i]) for i in (rng.integers(0, len(y), len(y)) for _ in range(n)) if 0 < y[i].sum() < len(i)]
    return roc_auc_score(y, p), np.percentile(b, 2.5), np.percentile(b, 97.5)


def main(vessels, outcome, features, covariates, test):
    extras = [f for f in features if f not in BASE_FEATURES] + covariates
    out = paths.REGRESSION.format(name=outcome.lower()) + "".join("_" + e.lower().replace(" ", "") for e in extras)
    os.makedirs(out, exist_ok=True)
    evals = ["val"] + (["test"] if test else [])
    for vessel in vessels:
        lines = []
        df, terms = load(vessel, outcome, features, covariates)
        tr = df[df.split == "train"]
        lines.append(f"{vessel} -> {outcome}: train {len(tr)} scans, {tr.y.mean():.1%} positive")
        pred = df[df.split.isin(["train"] + evals)][["case", "split", "y"]].copy()
        m = make_pipeline(StandardScaler(), LogisticRegression()).fit(tr[terms], tr.y)  # no tuning: nothing to select on val
        pred["p"] = m.predict_proba(df.loc[pred.index, terms])[:, 1]
        row = f"  train AUC {roc_auc_score(tr.y, pred.loc[tr.index, 'p']):.3f}"
        for s in evals:
            e = pred[pred.split == s]
            a, lo, hi = auc_ci(e.y.values, e.p.values)
            row += f" | {s} AUC {a:.3f} ({lo:.3f}-{hi:.3f}, n={len(e)})"
        lines += [row, "  odds ratio per SD: " + ", ".join(f"{c} {np.exp(v):.2f}" for c, v in zip(terms, m[-1].coef_[0]))]
        pred.to_csv(f"{out}/{vessel}_predictions.csv", index=False)
        open(f"{out}/{vessel}_summary.txt", "w").write("\n".join(lines) + "\n")
        print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--vessel", nargs="+", default=["LAD", "LCX", "RCA"], choices=["LAD", "LCX", "RCA"])
    ap.add_argument("--outcome", default="Disease")
    ap.add_argument("--features", nargs="+", default=BASE_FEATURES, help="per-vessel columns of the score CSVs")
    ap.add_argument("--covariates", nargs="*", default=[], help="per-scan columns of the descriptor sheets, e.g. Age Sex")
    ap.add_argument("--test", action="store_true", help="final run only: also report the test split")
    a = ap.parse_args()
    main(a.vessel, a.outcome, a.features, a.covariates, a.test)
