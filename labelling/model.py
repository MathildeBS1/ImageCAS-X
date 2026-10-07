"""Tree message-passing network and tree-consistent decoding for the segment labeller.

Plain torch; trees have tens of nodes, so no graph library. Each layer is SAGE-style with
separate weights for the node itself, its parent and the mean of its children, plus a residual
(CPR-GCN needed residuals; GraphSAGE-style updates beat GAT on a 141-patient coronary set).
``layers=0`` is the same model with no message passing, the reference that shows what the graph
adds. One head per side: left has 11 classes, right 3 (``data.CLASSES``).

Decoding is exact max-product over the rooted tree (Viterbi on a tree), with the network's
log-probabilities as unaries and Laplace-smoothed parent -> child transition counts from train
as soft penalties: hard rules from train transitions would force 7 test segments and 2 right
roots wrong by construction.
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from .data import CLASSES, Graph


class TreeGNN(nn.Module):
    def __init__(self, n_in: int, hidden: int = 128, layers: int = 3, dropout: float = 0.1):
        super().__init__()
        self.inp = nn.Sequential(nn.Linear(n_in, hidden), nn.ReLU(), nn.Linear(hidden, hidden))
        self.self_w = nn.ModuleList(nn.Linear(hidden, hidden) for _ in range(layers))
        self.par_w = nn.ModuleList(nn.Linear(hidden, hidden, bias=False) for _ in range(layers))
        self.ch_w = nn.ModuleList(nn.Linear(hidden, hidden, bias=False) for _ in range(layers))
        self.norm = nn.ModuleList(nn.LayerNorm(hidden) for _ in range(layers))
        self.drop = nn.Dropout(dropout)
        self.heads = nn.ModuleDict({s: nn.Linear(hidden, len(c)) for s, c in CLASSES.items()})

    def forward(self, x: torch.Tensor, parent: torch.Tensor) -> dict[str, torch.Tensor]:
        h = self.inp(x)
        has_par = (parent >= 0).float().unsqueeze(1)
        par = parent.clamp(min=0)
        kids = torch.zeros(len(x), device=x.device).index_add_(0, par, (parent >= 0).float())
        for ws, wp, wc, ln in zip(self.self_w, self.par_w, self.ch_w, self.norm):
            child_sum = torch.zeros_like(h).index_add_(0, par, h * has_par)
            child_mean = child_sum / kids.clamp(min=1).unsqueeze(1)
            h = h + self.drop(torch.relu(ln(ws(h) + wp(h[par]) * has_par + wc(child_mean))))
        return {s: head(h) for s, head in self.heads.items()}


def collate(graphs: list[Graph], mean: np.ndarray, std: np.ndarray):
    """One disjoint forest: standardised features, offset parents, targets, and the slice and
    side of each tree."""
    xs, ps, ys, sl, off = [], [], [], [], 0
    for g in graphs:
        xs.append((g.x - mean) / std)
        ps.append(np.where(g.parent >= 0, g.parent + off, -1))
        ys.append(g.y)
        sl.append((off, off + len(g.x), g.side))
        off += len(g.x)
    t = lambda a, d: torch.as_tensor(np.concatenate(a), dtype=d)
    return t(xs, torch.float32), t(ps, torch.long), t(ys, torch.long), sl


def transitions(graphs: list[Graph]) -> dict[str, dict[str, np.ndarray]]:
    """Per side, raw counts of parent -> child piece classes and of root classes."""
    out = {}
    for side, cls in CLASSES.items():
        T, root = np.zeros((len(cls), len(cls))), np.zeros(len(cls))
        for g in (g for g in graphs if g.side == side):
            for k, p in enumerate(g.parent):
                if g.y[k] < 0:
                    continue
                if p < 0:
                    root[g.y[k]] += 1
                elif g.y[p] >= 0:
                    T[g.y[p], g.y[k]] += 1
        out[side] = {"T": T, "root": root}
    return out


def viterbi(logp: np.ndarray, parent: np.ndarray, T: np.ndarray, root: np.ndarray) -> np.ndarray:
    """Most probable labelling of a tree. Nodes are in pre-order (parents first)."""
    logT = np.log((T + 1) / (T + 1).sum(1, keepdims=True))
    logR = np.log((root + 1) / (root + 1).sum())
    msg = logp.copy()
    best = np.zeros_like(logp, dtype=int)  # best child label given the parent's label
    for k in range(len(parent) - 1, -1, -1):
        p = parent[k]
        if p >= 0:
            s = logT + msg[k][None, :]  # [parent label, child label]
            best[k] = s.argmax(1)
            msg[p] += s.max(1)
    out = np.zeros(len(parent), dtype=int)
    for k in range(len(parent)):
        p = parent[k]
        out[k] = int(np.argmax(msg[k] + logR)) if p < 0 else best[k][out[p]]
    return out


def violation_rate(pred: np.ndarray, parent: np.ndarray, T: np.ndarray) -> float:
    """Share of parent -> child edges whose label pair never occurs in train."""
    e = [(parent[k], k) for k in range(len(parent)) if parent[k] >= 0]
    return float(np.mean([T[pred[p], pred[k]] == 0 for p, k in e])) if e else 0.0


def point_correct(g: Graph, pred: np.ndarray) -> tuple[float, float]:
    """(mm labelled correctly, mm with a label) over the tree's points; SPURIOUS points excluded."""
    cls = CLASSES[g.side]
    ok = tot = 0.0
    for k, (lab, w) in enumerate(zip(g.lab, g.w)):
        m = lab >= 0
        ok += float(w[m & (lab == cls[pred[k]])].sum())
        tot += float(w[m].sum())
    return ok, tot
