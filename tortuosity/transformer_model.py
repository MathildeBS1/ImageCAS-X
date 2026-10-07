"""Local-attention transformer on one vessel's ordered turning-angle profile, against the scalar
logistic regression on the same rows. After Tello Ayala et al., JACC: Advances 2026.

    python -m tortuosity.transformer_model --vessel LAD --outcome Disease   # fit on train, report val
    python -m tortuosity.transformer_model --chord 2                        # token-scale sensitivity
    python -m tortuosity.transformer_model --test                           # final run only

One token is the turning per mm at one interior vertex of the centerline after respacing to chord
`--chord` mm (`curvature.profile`), in the thesis's own rad/mm and not divided by pi as Tello Ayala
et al. do, so the sequence's mean is exactly T_5. Both arms therefore see the same measurement, the
transformer as the ordered profile and the baseline as its mean, with nothing else differing: the
baseline's terms are T_5 and length_mm, the transformer's are the profile and length_mm. Both are
fitted on the same rows, so the AUC difference carries a paired bootstrap CI, which the paper does
not report for its own 0.67 against 0.60. The angle channel is standardised on the training tokens,
so the unit it is carried in cannot change the result.

Needs torch (CPU is enough):
    uv pip install torch --index-url https://download.pytorch.org/whl/cpu

Deviations from the paper, none of them avoidable here:
- the architecture is ours. The paper states no layers, heads, loss or split, and releases no code.
- 3D CTA centerlines, not 2D LAO projections of invasive angiograms.
- tokens respaced to a stated chord, not the native skeleton spacing of a 2D mask, and carried in
  rad/mm, per `thesis/week5/rca_tortuosity.tex`, not as the angle over pi.
- the outcome is scan-level `Disease` from Descriptors.xlsx (800 scans, 388 yes), not a per-vessel
  stenosis call by the cardiologist reading the same image. One vessel's profile is therefore asked
  about the whole scan, and the paper's label circularity is not inherited.
- 560 training scans against their 38,691 angiograms, and 80 val scans, whose AUC CI is about 0.13
  wide. A gap the size of theirs cannot be resolved at this n: read the CIs before the point
  estimates, and treat a null as unresolved, not as evidence against the profile.
- Descriptors.xlsx carries no age or sex, so the paper's two covariates are absent; --covariates is
  the hook once a sheet has them.
"""
import argparse
import os
from functools import lru_cache

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from torch import nn

from . import paths
from .curvature import profile
from .regression_model import BASE_FEATURES, SEED, auc_ci, load
from .vessels import load_vessels

# written into every summary, since nothing here is selected on data
HP = dict(d_model=32, nhead=4, layers=2, ffn=64, dropout=0.2, window=3, lr=3e-3, wd=1e-2, epochs=200, seeds=5)


@lru_cache(maxsize=None)
def profiles(case, chord):
    """{name: per-point profile} for one scan, cached so each VTK pair is read once per run."""
    return {k: profile(P, chord) for k, P in load_vessels(case).items()}


def sequences(df, vessel, chord):
    """Padded profiles (n, T, 2), the pad mask (n, T), the rows kept, and the cases dropped.

    Channel 0 is the angle, channel 1 the relative position along the vessel, so a bend's place is
    comparable across vessels of different length. A row with no usable profile is dropped from df
    and returned, which keeps this arm's cohort identical to the baseline's.
    """
    seq, keep, dropped = [], [], []
    for i, case in zip(df.index, df.case):
        a = profiles(case, chord).get(vessel)
        if a is None or len(a) < 2:
            dropped.append(case)
            continue
        seq.append(a)
        keep.append(i)
    T = max(len(a) for a in seq)
    x, pad = np.zeros((len(seq), T, 2), np.float32), np.ones((len(seq), T), bool)
    for i, a in enumerate(seq):
        x[i, :len(a), 0], x[i, :len(a), 1] = a, np.linspace(0, 1, len(a))
        pad[i, :len(a)] = False
    return torch.tensor(x), torch.tensor(pad), df.loc[keep].reset_index(drop=True), dropped


def attn_mask(pad, window, nhead):
    """(n * nhead, T, T) mask: a token sees its +-window neighbours and never a padded one.

    A padded query keeps its own diagonal. Without it its softmax has no unmasked key and returns
    nan, which the next layer would spread to the real tokens through a zero weight.
    """
    i = torch.arange(pad.shape[1])
    m = ((i[:, None] - i[None, :]).abs() > window)[None] | pad[:, None, :]
    return (m & ~torch.eye(pad.shape[1], dtype=torch.bool)).repeat_interleave(nhead, 0)


class ProfileTransformer(nn.Module):
    """Local-attention encoder over the profile, mean-pooled and joined to the scalar terms."""

    def __init__(self, n_scalar, hp):
        super().__init__()
        self.hp = hp
        self.embed = nn.Linear(2, hp["d_model"])
        layer = nn.TransformerEncoderLayer(hp["d_model"], hp["nhead"], hp["ffn"], hp["dropout"],
                                           batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(layer, hp["layers"], enable_nested_tensor=False)
        self.head = nn.Linear(hp["d_model"] + n_scalar, 1)

    def forward(self, x, pad, s, mask):
        h = self.encoder(self.embed(x), mask=mask)
        h = (h * ~pad[..., None]).sum(1) / (~pad).sum(1, keepdim=True)  # masked mean; padded rows zeroed
        return self.head(torch.cat([h, s], 1)).squeeze(1)


def fit_predict(x, pad, s, y, train, hp, seed):
    """Probabilities for every row, from a model fitted on the train rows alone."""
    torch.manual_seed(seed)
    m = ProfileTransformer(s.shape[1], hp)
    opt = torch.optim.AdamW(m.parameters(), lr=hp["lr"], weight_decay=hp["wd"])
    bce = nn.BCEWithLogitsLoss()
    mask, mask_tr = (attn_mask(p, hp["window"], hp["nhead"]) for p in (pad, pad[train]))  # fixed by pad, so built once
    for _ in range(hp["epochs"]):  # full batch, so one step per epoch
        opt.zero_grad()
        bce(m(x[train], pad[train], s[train], mask_tr), y[train]).backward()
        opt.step()
    m.eval()
    with torch.no_grad():
        return torch.sigmoid(m(x, pad, s, mask)).numpy()


def diff_ci(y, p1, p2, n=2000):
    """AUC(p1) - AUC(p2) with a bootstrap CI over scans, one resample shared by both arms."""
    rng = np.random.default_rng(SEED)
    b = [roc_auc_score(y[i], p1[i]) - roc_auc_score(y[i], p2[i])
         for i in (rng.integers(0, len(y), len(y)) for _ in range(n)) if 0 < y[i].sum() < len(i)]
    return roc_auc_score(y, p1) - roc_auc_score(y, p2), np.percentile(b, 2.5), np.percentile(b, 97.5)


def main(vessels, outcome, covariates, chord, test, hp):
    name = outcome.lower() + ("" if chord == 5 else f"_chord{chord:g}")
    out = (paths.TRANSFORMER.format(name=name) + "".join("_" + c.lower().replace(" ", "") for c in covariates)
           + "".join(f"_{k}{v:g}" for k, v in hp.items() if v != HP[k]))  # so a shorter run never overwrites a full one
    os.makedirs(out, exist_ok=True)
    evals = ["val"] + (["test"] if test else [])
    fails = []
    for vessel in vessels:
        df, terms = load(vessel, outcome, BASE_FEATURES, covariates)
        x, pad, df, dropped = sequences(df, vessel, chord)
        fails += [f"{vessel}\t{c}\tno profile at chord {chord} mm\n" for c in dropped]
        side = [t for t in terms if t != "T_5"]  # T_5 is what the baseline gets in place of the profile
        tr = (df.split == "train").values
        a = x[torch.tensor(tr), :, 0][~pad[torch.tensor(tr)]]  # the training tokens, padding left out
        x[:, :, 0] = (x[:, :, 0] - a.mean()) / a.std()  # so rad/mm against angle over pi cannot matter
        s = torch.tensor(StandardScaler().fit(df[side][tr]).transform(df[side]), dtype=torch.float32)
        y = torch.tensor(df.y.values, dtype=torch.float32)

        p_t = np.mean([fit_predict(x, pad, s, y, torch.tensor(tr), hp, SEED + k) for k in range(hp["seeds"])], 0)
        m = make_pipeline(StandardScaler(), LogisticRegression()).fit(df[terms][tr], df.y[tr])  # the same baseline
        p_l = m.predict_proba(df[terms])[:, 1]

        lines = [f"{vessel} -> {outcome}: train {tr.sum()} scans, {df.y[tr].mean():.1%} positive",
                 f"  chord {chord} mm: {int(np.median((~pad).sum(1)))} tokens at the median, {x.shape[1]} at most"]
        for split in ["train"] + evals:
            e = (df.split == split).values
            at, alo, ahi = auc_ci(df.y[e].values, p_t[e])
            al, llo, lhi = auc_ci(df.y[e].values, p_l[e])
            d, dlo, dhi = diff_ci(df.y[e].values, p_t[e], p_l[e])
            lines.append(f"  {split:<5} n={e.sum():<4} profile AUC {at:.3f} ({alo:.3f}-{ahi:.3f})"
                         f" | scalar AUC {al:.3f} ({llo:.3f}-{lhi:.3f})"
                         f" | difference {d:+.3f} ({dlo:+.3f}-{dhi:+.3f}), paired")
        lines.append("  " + ", ".join(f"{k} {v}" for k, v in hp.items()) + f" of {SEED}..{SEED + hp['seeds'] - 1}")
        pred = df.assign(p_transformer=p_t, p_logistic=p_l)
        pred[pred.split.isin(["train"] + evals)][["case", "split", "y", "p_transformer", "p_logistic"]].to_csv(
            f"{out}/{vessel}_predictions.csv", index=False)
        open(f"{out}/{vessel}_summary.txt", "w").write("\n".join(lines) + "\n\n" + __doc__)
        print("\n".join(lines))
    open(f"{out}/failed.txt", "w").writelines(fails)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--vessel", nargs="+", default=["LAD", "LCX", "RCA"], choices=["LAD", "LCX", "RCA"])
    ap.add_argument("--outcome", default="Disease")
    ap.add_argument("--covariates", nargs="*", default=[], help="per-scan columns of the descriptor sheets")
    ap.add_argument("--chord", type=float, default=5, help="mm per token; 5 matches the reported T_5")
    ap.add_argument("--test", action="store_true", help="final run only: also report the test split")
    for k, v in HP.items():
        ap.add_argument(f"--{k}", type=type(v), default=v)
    a = ap.parse_args()
    main(a.vessel, a.outcome, a.covariates, a.chord, a.test, {k: getattr(a, k) for k in HP})
