"""Train the segment labeller on delivered train trees, early-stopping on delivered val.

    python -m labelling.train --run gnn3
    python -m labelling.train --run gnn0 --layers 0      # no-message-passing reference

Needs ``python -m labelling.data --source delivered --split {train,val}`` first. Writes
``RESULTS/labeller/<run>/{model.pt,log.csv}``; ``model.pt`` holds the weights, the feature
standardisation, the train transition counts and the arguments, so ``evaluate.py`` needs nothing
else. Loss is class-weighted cross-entropy (inverse square-root piece frequency per side: L-PDA
has 37 train segments against 1546 for LAD). Selection is on length-weighted point accuracy.
"""

from __future__ import annotations

import argparse
import time

import numpy as np
import torch
from torch import nn

from bifurcation import paths
from utils.seeding import SEED, seed_everything

from . import data, model

OUT = paths.RESULTS / "labeller"


def _accuracy(net, graphs, mean, std) -> float:
    net.eval()
    ok = tot = 0.0
    with torch.no_grad():
        x, par, _, sl = model.collate(graphs, mean, std)
        logits = net(x, par)
        for g, (a, b, side) in zip(graphs, sl):
            o, t = model.point_correct(g, logits[side][a:b].argmax(1).numpy())
            ok, tot = ok + o, tot + t
    return ok / tot


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--layers", type=int, default=3)
    ap.add_argument("--hidden", type=int, default=128)
    ap.add_argument("--epochs", type=int, default=400)
    ap.add_argument("--patience", type=int, default=50)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-3)
    args = ap.parse_args()
    seed_everything()
    rng = np.random.default_rng(SEED)
    out = OUT / args.run
    out.mkdir(parents=True, exist_ok=True)

    train = [s for *_, s in data.load("delivered", "train") if s]
    val = [data.featurize(s, side) for _, side, s in data.load("delivered", "val") if s]
    sides = [side for _, side, s in data.load("delivered", "train") if s]
    plain = [data.featurize(s, side) for s, side in zip(train, sides)]
    allx = np.concatenate([g.x for g in plain])
    mean, std = allx.mean(0), allx.std(0) + 1e-6
    trans = model.transitions(plain)
    weights = {}
    for side, cls in data.CLASSES.items():
        n = np.bincount(np.concatenate([g.y[g.y >= 0] for g in plain if g.side == side]), minlength=len(cls))
        weights[side] = torch.tensor(1 / np.sqrt(np.maximum(n, 1)), dtype=torch.float32)
        weights[side] *= len(cls) / weights[side].sum()
    loss_fn = {s: nn.CrossEntropyLoss(weight=w, ignore_index=-1) for s, w in weights.items()}
    print(f"train {len(train)} trees, val {len(val)}; features {allx.shape[1]}", flush=True)

    net = model.TreeGNN(allx.shape[1], args.hidden, args.layers)
    opt = torch.optim.AdamW(net.parameters(), lr=args.lr, weight_decay=1e-4)
    best, best_epoch, log = -1.0, 0, ["epoch,loss,val_acc,seconds"]
    for epoch in range(args.epochs):
        t0, net = time.time(), net.train()
        order, losses = rng.permutation(len(train)), []
        for i in range(0, len(order), args.batch):
            graphs = [data.featurize(data.augment(train[k], rng), sides[k]) for k in order[i:i + args.batch]]
            x, par, y, sl = model.collate(graphs, mean, std)
            logits = net(x, par)
            loss = 0.0
            for side in data.CLASSES:
                idx = torch.cat([torch.arange(a, b) for a, b, s in sl if s == side] or [torch.zeros(0, dtype=torch.long)])
                if len(idx):
                    loss = loss + loss_fn[side](logits[side][idx], y[idx]) * len(idx) / len(y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.detach()))
        acc = _accuracy(net, val, mean, std)
        log.append(f"{epoch},{np.mean(losses):.4f},{acc:.4f},{time.time() - t0:.1f}")
        print(log[-1], flush=True)
        if acc > best:
            best, best_epoch = acc, epoch
            torch.save({"state_dict": net.state_dict(), "mean": mean, "std": std, "transitions": trans,
                        "args": vars(args), "n_in": allx.shape[1], "epoch": epoch, "val_acc": acc},
                       out / "model.pt")
        elif epoch - best_epoch >= args.patience:
            break
        (out / "log.csv").write_text("\n".join(log) + "\n")
    (out / "log.csv").write_text("\n".join(log) + "\n")
    print(f"best val point accuracy {best:.4f} at epoch {best_epoch} -> {out / 'model.pt'}")


if __name__ == "__main__":
    main()
