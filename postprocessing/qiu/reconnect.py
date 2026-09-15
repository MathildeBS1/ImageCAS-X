"""Qiu et al. stage 2 end to end on one binary prediction: which fragments to join where
(section 3.3.1), the walk (3.3.2, walk.py), whether to trust it (3.3.3), and writing
the result back into the mask.

Geometry: the prediction arrives on the scan's native grid, where Betti numbers are
scored. Its 26-connected components are labelled there, and the label map is
nearest-neighbour resampled onto the 0.5 mm grid of the offline cache (the grid
CAS-Net itself predicted on), where skeletons, walks and the classifier run. Only
two things are written back to the native mask: fragments that are removed (by their
native label, so nothing else moves), and tubes painted along accepted paths. Every
other voxel of the prediction is left bit-identical.

Units: every threshold in `ReconnectParams` is in mm. The paper states them in voxels
of ASOCA/PDSCA (in-plane 0.3-0.4 mm); they were converted at a nominal 0.4 mm/voxel.
Patch and neighbourhood sizes stay in voxels, now 0.5 mm ones.
"""
import time
import warnings
from dataclasses import dataclass, field, fields

import numpy as np
import SimpleITK as sitk
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

from postprocessing.qiu import skeleton as sk
from postprocessing.qiu.classifier import CenterlineProbability, normalise_hu
from postprocessing.qiu.walk import dpc_walk, _unit
from utils import io as bio

_CONN26 = np.ones((3, 3, 3), dtype=bool)


@dataclass
class ReconnectParams:
    mode: str = "qiu"                       # "qiu" | "keep_largest" (baseline, no joins)
    n_main_components: int = 2              # "the two largest connected components"
    grid_mm: float = 0.5
    remove_unconnected: bool = True         # paper: failed fragments are eliminated
    enable_type1: bool = True
    enable_type2: bool = True
    enable_type3: bool = True
    # 3.3.1 candidate filtering (paper voxels x 0.4 mm)
    type1_max_dist_mm: float = 24.0         # 60 voxels
    type2_max_dist_mm: float = 32.0         # 80 voxels
    max_proximal_angle_deg: float = 120.0
    positional_cos_floor: float = 1.6
    type3_short_len_mm: float = 4.0         # length > 10 voxels ...
    type3_short_dist_mm: float = 8.0        # ... -> nearest distance < 20 voxels
    type3_long_len_mm: float = 20.0         # length > 50 voxels ...
    type3_long_dist_mm: float = 32.0        # ... -> nearest distance < 80 voxels
    max_candidates: int = 2
    # 3.3.2 walk
    omega: float = 5.0
    second_level_min_gap_mm: float = 5.0    # not given in the paper
    max_steps_factor: float = 3.0           # not given in the paper
    direction_points: int = 3
    spur_min_len_vox: int = 4               # not in the paper; see skeleton._prune_spurs
    # 3.3.3 evaluation
    eval_threshold: float = 1.0             # paper: "a predefined threshold (e.g., 1)"
    use_adf: bool = True
    adf_context_vox: int = 5
    adf_min_length: int = 8                 # below this the ADF term is not applied
    max_rounds: int = 3
    # stage 3 substitute
    min_tube_radius_mm: float = 0.6

    @classmethod
    def from_dict(cls, d: dict) -> "ReconnectParams":
        names = {f.name for f in fields(cls)}
        unknown = set(d) - names
        if unknown:
            raise ValueError(f"Unknown reconnection params: {sorted(unknown)}")
        return cls(**{k: v for k, v in d.items() if k in names})


@dataclass
class _Structure:
    """A main tree, or a group of fragments already joined to each other."""
    labels: set
    cl: sk.Centerline
    joins: list = field(default_factory=list)   # accepted paths, for painting
    attached_to: int | None = None


def adf_pvalue(x: np.ndarray, min_length: int) -> tuple[float, str]:
    """Augmented Dickey-Fuller p-value (H0: unit root, i.e. non-stationary). A low
    p-value is evidence the sequence is stationary, as along one continuous vessel."""
    from statsmodels.tsa.stattools import adfuller

    x = np.asarray(x, dtype=float)
    if len(x) < min_length:
        return 0.0, "too_short"
    if np.std(x) < 1e-6:
        return 0.0, "constant"
    maxlag = max(0, min(int(12 * (len(x) / 100) ** 0.25), len(x) // 3 - 1))
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")   # statsmodels' return-type FutureWarning
            return float(adfuller(x, maxlag=maxlag, autolag="AIC")[1]), "ok"
    except Exception as e:  # singular regressions on degenerate sequences
        return 0.0, f"failed: {e}"


class Reconnector:
    def __init__(self, params: ReconnectParams, model=None):
        self.p = params
        self.model = model

    # ------------------------------------------------------------------ geometry --
    def _to_grid(self, lab_nat: np.ndarray, ref_img) -> np.ndarray:
        img = sitk.GetImageFromArray(lab_nat.transpose(2, 1, 0).astype(np.int32))
        img.CopyInformation(ref_img)
        r = sitk.ResampleImageFilter()
        r.SetReferenceImage(bio.resampled_geometry(ref_img, self.p.grid_mm))
        r.SetInterpolator(sitk.sitkNearestNeighbor)
        r.SetDefaultPixelValue(0)
        return sitk.GetArrayFromImage(r.Execute(img)).transpose(2, 1, 0)

    def _paint_tube(self, out: np.ndarray, path: np.ndarray, r0: float, r1: float,
                    spacing: np.ndarray):
        """Stage 3 substitute: fill the stitched path on the native grid as a tube whose
        radius runs linearly from the fragment's radius to the target's."""
        pts = path.astype(float) * self.p.grid_mm            # mm along the image axes
        seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        cum = np.concatenate([[0.0], np.cumsum(seg)])
        s = np.linspace(0.0, cum[-1], max(2, int(np.ceil(cum[-1] / 0.2)) + 1))
        dense = np.stack([np.interp(s, cum, pts[:, i]) for i in range(3)], axis=1)
        radii = np.maximum(self.p.min_tube_radius_mm,
                           r0 + (r1 - r0) * s / max(cum[-1], 1e-9))
        shape = np.array(out.shape)
        for c, r in zip(dense, radii):
            lo = np.clip(np.floor((c - r) / spacing).astype(int), 0, shape - 1)
            hi = np.clip(np.ceil((c + r) / spacing).astype(int), 0, shape - 1)
            g = np.stack(np.meshgrid(*[np.arange(lo[i], hi[i] + 1) for i in range(3)],
                                     indexing="ij"), axis=-1)
            inside = (((g * spacing - c) ** 2).sum(-1) <= r * r)
            sel = g[inside]
            out[sel[:, 0], sel[:, 1], sel[:, 2]] = 1

    # ---------------------------------------------------------------- candidates --
    @staticmethod
    def _head_toward(g: _Structure, target: np.ndarray) -> sk.Endpoint:
        """The fragment tip nearest `target`. A fragment too small to have a tip gets
        a synthetic one at its nearest skeleton voxel, pointing along its principal
        axis (signed toward the target)."""
        if g.cl.endpoints:
            return min(g.cl.endpoints, key=lambda e: np.linalg.norm(e.point - target))
        _, i = g.cl.tree.query(target)
        pt = g.cl.points[i]
        axis = g.cl.axis if np.dot(g.cl.axis, target - pt) >= 0 else -g.cl.axis
        return sk.Endpoint(point=pt, direction=axis, radius_mm=float(g.cl.radius_mm[i]),
                           branch=pt[None])

    def _tip_facing(self, g: _Structure, other: sk.Centerline) -> sk.Endpoint:
        """The tip of `g` nearest any point of `other`."""
        if g.cl.endpoints:
            return min(g.cl.endpoints, key=lambda e: other.tree.query(e.point)[0])
        d, i = other.tree.query(g.cl.points)
        return self._head_toward(g, other.points[i[int(np.argmin(d))]])

    def _angles(self, tail: sk.Endpoint, head: sk.Endpoint) -> tuple[float, float]:
        """(cos proximal angle, sum of positional cosines), directions taken along
        the flow: out of the tail, into the head."""
        u_t, u_h_in = tail.direction, -head.direction
        conn = _unit((head.point - tail.point).astype(float))
        return float(u_t @ u_h_in), float(conn @ u_t + conn @ u_h_in)

    def _type2_candidates(self, g: _Structure, mains: list, exclude: set) -> list:
        p, out = self.p, []
        cos_max = np.cos(np.deg2rad(p.max_proximal_angle_deg))
        for mi, m in enumerate(mains):
            for tail in m.cl.endpoints:
                if (mi, _branch_key(tail.branch)) in exclude:
                    continue
                d = cKDTree(tail.branch).query(g.cl.points)[0].min() * p.grid_mm
                if d >= p.type2_max_dist_mm:
                    continue
                head = self._head_toward(g, tail.point)
                cos_prox, cos_pos = self._angles(tail, head)
                if cos_prox > cos_max and cos_pos > min(p.positional_cos_floor, 2 * cos_prox):
                    out.append(dict(type=2, main=mi, tail=tail, head=head, dist_mm=float(d),
                                    cos_proximal=cos_prox, cos_positional=cos_pos,
                                    key=(mi, _branch_key(tail.branch))))
        return sorted(out, key=lambda c: c["dist_mm"])[:p.max_candidates]

    def _type3_candidates(self, g: _Structure, mains: list, exclude: set) -> list:
        """Every main-tree branch near a long-enough fragment, including interior ones.
        The paper says only that type 3's angle settings are "reversed compared to Type
        2"; this reads that as: whatever type 2's angle test did not already send
        somewhere. Branches already tried (as type 2 or in an earlier round) are in
        `exclude`."""
        p = self.p
        length = g.cl.length_vox() * p.grid_mm
        if length > p.type3_long_len_mm:
            max_d = p.type3_long_dist_mm
        elif length > p.type3_short_len_mm:
            max_d = p.type3_short_dist_mm
        else:
            return []
        out = []
        for mi, m in enumerate(mains):
            for b in m.cl.branches:
                if len(b) < 2 or (mi, _branch_key(b)) in exclude:
                    continue
                tree = cKDTree(b)
                dists = tree.query(g.cl.points)[0]
                d = dists.min() * p.grid_mm
                if d >= max_d:
                    continue
                nearest = g.cl.points[int(np.argmin(dists))]
                head = self._head_toward(g, b[tree.query(nearest)[1]])
                out.append(dict(type=3, main=mi, branch=b, branch_tree=tree, head=head,
                                dist_mm=float(d), frag_len_mm=float(length),
                                key=(mi, _branch_key(b))))
        return sorted(out, key=lambda c: c["dist_mm"])[:p.max_candidates]

    # -------------------------------------------------------------- walk + check --
    def _attempt(self, g: _Structure, cand: dict, target: _Structure, others: list,
                 lab05: np.ndarray, n_labels: int, prob, vol_n: np.ndarray,
                 blocked: set) -> dict:
        p = self.p
        head = cand["head"]
        reached = np.zeros(n_labels + 1, dtype=bool)
        reached[list(target.labels)] = True
        forbidden = np.zeros(n_labels + 1, dtype=bool)
        for o in others:
            forbidden[list(o.labels)] = True

        if cand["type"] == 3:
            gap = cand["branch_tree"].query(head.point)[0]
            kw = dict(target_point=None, target_tree=cand["branch_tree"])
        else:
            gap = float(np.linalg.norm(cand["tail"].point - head.point))
            kw = dict(target_point=cand["tail"].point.astype(float), target_tree=None)
        second = gap * p.grid_mm > p.second_level_min_gap_mm
        max_steps = int(p.max_steps_factor * gap / (2.0 if second else 1.0)) + 10

        res = dpc_walk(head.point, head.direction, reached_label=reached, label_volume=lab05,
                       forbidden_label=forbidden, prob=prob, blocked=blocked, omega=p.omega,
                       second_level=second, max_steps=max_steps, **kw)
        rec = dict(type=cand["type"], dist_mm=cand["dist_mm"], gap_mm=float(gap * p.grid_mm),
                   second_level=bool(second), walk=res.reason, steps=len(res.path) - 1)
        for k in ("cos_proximal", "cos_positional", "frag_len_mm"):
            if k in cand:
                rec[k] = cand[k]
        if not res.reached:
            rec["accepted"] = False
            return rec

        # 3.3.3: mean P along the stitched path + mean P along CL_j, against a
        # threshold raised by the ADF p-values of the path's P and grey sequences.
        path = res.path
        p_path = prob(path[1:])
        p_frag = prob(g.cl.points)
        k = p.adf_context_vox
        _, ti = target.cl.tree.query(path[-1], k=min(k, len(target.cl.points)))
        _, hi = g.cl.tree.query(path[0], k=min(k, len(g.cl.points)))
        ti, hi = np.atleast_1d(ti), np.atleast_1d(hi)
        seq = np.concatenate([target.cl.points[ti][::-1], path[::-1], g.cl.points[hi]])
        grey = vol_n[seq[:, 0], seq[:, 1], seq[:, 2]]
        adf_p, adf_p_status = adf_pvalue(p_path, p.adf_min_length)
        adf_g, adf_g_status = adf_pvalue(grey, p.adf_min_length)
        score = float(p_path.mean() + p_frag.mean())
        needed = p.eval_threshold + (adf_p + adf_g if p.use_adf else 0.0)
        rec.update(mean_p_path=float(p_path.mean()), mean_p_fragment=float(p_frag.mean()),
                   adf_p_prob=adf_p, adf_p_prob_status=adf_p_status,
                   adf_p_grey=adf_g, adf_p_grey_status=adf_g_status,
                   score=score, needed=float(needed), accepted=bool(score >= needed))
        rec["_path"] = path          # kept for rejected walks too, for GT annotation
        if rec["accepted"]:
            rec["_r0"] = g.cl.radius_at(path[0])
            rec["_r1"] = target.cl.radius_at(path[-1])
        return rec

    @staticmethod
    def _join(into: _Structure, g: _Structure, rec: dict, used: list):
        """Absorb `g` into `into`; the joined tips stop being tips."""
        path = rec["_path"]
        radii = np.linspace(rec["_r0"], rec["_r1"], len(path))
        cl = sk.merge([into.cl, g.cl], [path], [radii])
        cl.endpoints = [e for e in cl.endpoints
                        if not any(np.array_equal(e.point, u.point) for u in used)]
        into.cl = cl
        into.labels |= g.labels
        into.joins += g.joins + [rec]

    # ---------------------------------------------------------------------- run --
    def __call__(self, pred: np.ndarray, ref_img, volume_hu: np.ndarray | None,
                 gt: np.ndarray | None = None) -> tuple:
        """Repair `pred` (native grid). `gt`, if given, is used only AFTER every decision
        has been made, to annotate the log with whether each fragment and each walked
        path lies in the true lumen. It never reaches a decision."""
        t0 = time.time()
        p = self.p
        pred = (pred > 0).astype(np.uint8)
        lab_nat, n = ndi.label(pred, structure=_CONN26)
        log = dict(b0_before=int(n), mode=p.mode, fragments=[], attempts_type1=[], attempts=[])
        if n <= p.n_main_components:
            log.update(b0_after=int(n), note="no fragments", seconds=time.time() - t0)
            return pred, log

        sizes = np.bincount(lab_nat.ravel())[1:]
        order = np.argsort(sizes)[::-1] + 1
        main_ids, frag_ids = order[:p.n_main_components], order[p.n_main_components:]
        log["main_sizes_vox"] = sizes[main_ids - 1].tolist()

        if p.mode == "keep_largest":
            out = np.isin(lab_nat, main_ids).astype(np.uint8)
            fragments = [dict(label=int(f), size_vox=int(sizes[f - 1]), decision="removed")
                         for f in frag_ids]
            if gt is not None:
                gt_dil = ndi.binary_dilation(gt > 0, structure=_CONN26)
                for fr, fx in zip(fragments, np.atleast_1d(ndi.mean(gt_dil, lab_nat, index=frag_ids))):
                    fr["gt_fraction"] = float(fx)
            log.update(b0_after=int(ndi.label(out, structure=_CONN26)[1]),
                       n_fragments=int(len(frag_ids)), fragments=fragments,
                       n_fragments_removed=int(len(frag_ids)), seconds=time.time() - t0)
            return out, log
        if p.mode != "qiu":
            raise ValueError(f"Unknown reconnection mode '{p.mode}'")
        if self.model is None or volume_hu is None:
            raise ValueError("mode 'qiu' needs the centerline classifier and the 0.5 mm volume")

        lab05 = self._to_grid(lab_nat, ref_img)
        if lab05.shape != volume_hu.shape:
            raise ValueError(f"0.5 mm label grid {lab05.shape} != cached volume {volume_hu.shape}")
        vol_n = normalise_hu(volume_hu)
        prob = CenterlineProbability(self.model, vol_n)
        slices = ndi.find_objects(lab05)

        def centerline(labels) -> sk.Centerline | None:
            parts = []
            for lb in labels:
                sl = slices[lb - 1] if lb - 1 < len(slices) else None
                if sl is None:
                    continue
                parts.append(sk.build_centerline(
                    lab05[sl] == lb, np.array([s.start for s in sl]), p.grid_mm,
                    p.spur_min_len_vox, p.direction_points))
            return sk.merge(parts) if parts else None

        mains = [_Structure(labels={int(m)}, cl=centerline([m])) for m in main_ids]
        groups, vanished = [], []
        for f in frag_ids:
            cl = centerline([f])
            if cl is None:
                vanished.append(int(f))     # too small to survive the 0.5 mm grid; never
                                            # a join candidate, handled like a failed one
            else:
                groups.append(_Structure(labels={int(f)}, cl=cl))
        blocked: set = set()

        def dist_to_mains(g):
            return min(m.cl.tree.query(g.cl.points)[0].min() for m in mains)

        # Type 1: fragments joined to each other first, so two fragments heading for
        # the same tree do not each lay their own overlapping path.
        attempts_t1 = []
        if p.enable_type1:
            tried_pairs = set()
            cos_max = np.cos(np.deg2rad(p.max_proximal_angle_deg))
            while True:
                pairs = []
                for i in range(len(groups)):
                    for j in range(i + 1, len(groups)):
                        key = (frozenset(groups[i].labels), frozenset(groups[j].labels))
                        if key in tried_pairs:
                            continue
                        d = groups[i].cl.tree.query(groups[j].cl.points)[0].min() * p.grid_mm
                        if d < p.type1_max_dist_mm:
                            pairs.append((d, i, j, key))
                if not pairs:
                    break
                d, i, j, key = min(pairs)
                tried_pairs.add(key)
                a, b = groups[i], groups[j]
                if dist_to_mains(b) < dist_to_mains(a):
                    a, b = b, a                    # a: nearer the trees, holds the tail
                tail = self._tip_facing(a, b.cl)
                head = self._head_toward(b, tail.point)
                cos_prox, cos_pos = self._angles(tail, head)
                if cos_prox <= cos_max:
                    continue
                cand = dict(type=1, tail=tail, head=head, dist_mm=float(d),
                            cos_proximal=cos_prox, cos_positional=cos_pos)
                rec = self._attempt(b, cand, a, mains, lab05, n, prob, vol_n, blocked)
                rec["labels"] = sorted(a.labels | b.labels)
                attempts_t1.append(rec)
                if rec["accepted"]:
                    blocked.update(map(tuple, rec["_path"]))
                    self._join(a, b, rec, [tail, head])
                    groups.remove(b)

        # Type 2 over every waiting fragment, then type 3 over those still waiting (the
        # paper performs the three types "sequentially ... on all input centerline
        # branches"), repeated over rounds: a fragment joined in one round offers its
        # own tips as tails to those still waiting. A (fragment, branch) pair is walked
        # at most once across all rounds and both types.
        attempts, tried = [], set()
        for rnd in range(p.max_rounds):
            changed = False
            for kind, enabled in ((2, p.enable_type2), (3, p.enable_type3)):
                if not enabled:
                    continue
                for g in sorted([g for g in groups if g.attached_to is None], key=dist_to_mains):
                    gkey = frozenset(g.labels)
                    done = {k for (gk, k) in tried if gk == gkey}
                    cands = (self._type2_candidates(g, mains, done) if kind == 2
                             else self._type3_candidates(g, mains, done))
                    for c in cands:
                        tried.add((gkey, c["key"]))
                        others = [m for i, m in enumerate(mains) if i != c["main"]]
                        rec = self._attempt(g, c, mains[c["main"]], others, lab05, n, prob,
                                            vol_n, blocked)
                        rec.update(round=rnd + 1, labels=sorted(g.labels), main=c["main"])
                        attempts.append(rec)
                        if rec["accepted"]:
                            blocked.update(map(tuple, rec["_path"]))
                            used = [c["head"]] + ([c["tail"]] if "tail" in c else [])
                            g.attached_to = c["main"]
                            self._join(mains[c["main"]], g, rec, used)
                            changed = True
                            break
            if not changed:
                break

        # Write back to the native grid.
        spacing = np.array(ref_img.GetSpacing(), dtype=float)
        out = pred.copy()
        drop = np.zeros(n + 1, dtype=bool)
        drop[vanished] = p.remove_unconnected
        unattached = [g for g in groups if g.attached_to is None]
        for g in unattached:
            if p.remove_unconnected:
                drop[list(g.labels)] = True
        out[drop[lab_nat]] = 0
        painted = [m.joins for m in mains] + ([] if p.remove_unconnected
                                              else [g.joins for g in unattached])
        for joins in painted:
            for rec in joins:
                self._paint_tube(out, rec["_path"], rec["_r0"], rec["_r1"], spacing)

        decision = {int(f): "removed" if p.remove_unconnected else "kept" for f in frag_ids}
        for mi, m in enumerate(mains):
            for lb in m.labels - {int(main_ids[mi])}:
                decision[lb] = "attached"
        fragments = [dict(label=int(f), size_vox=int(sizes[f - 1]), decision=decision[int(f)],
                          vanished_on_grid=int(f) in vanished) for f in frag_ids]

        if gt is not None:
            # Diagnostics only: every decision above is already final.
            gt_dil = ndi.binary_dilation(gt > 0, structure=_CONN26)
            frac = ndi.mean(gt_dil, lab_nat, index=frag_ids)
            for fr, fx in zip(fragments, np.atleast_1d(frac)):
                fr["gt_fraction"] = float(fx)
            scale = self.p.grid_mm / spacing
            shape = np.array(gt_dil.shape)
            for rec in attempts_t1 + attempts:
                if "_path" in rec:
                    idx = np.clip(np.round(rec["_path"] * scale).astype(int), 0, shape - 1)
                    rec["path_in_gt_fraction"] = float(gt_dil[tuple(idx.T)].mean())

        log.update(
            n_fragments=int(len(frag_ids)),
            fragments=fragments,
            vanished_on_grid=vanished,
            attempts_type1=[_public(r) for r in attempts_t1],
            attempts=[_public(r) for r in attempts],
            n_joined=int(sum(len(m.joins) for m in mains)),
            n_fragments_attached=int(sum(len(m.labels) - 1 for m in mains)),
            n_fragments_removed=int(drop.sum()) if p.remove_unconnected else 0,
            b0_after=int(ndi.label(out, structure=_CONN26)[1]),
            p_evaluations=len(prob.cache),
            seconds=round(time.time() - t0, 1),
        )
        return out, log


def _branch_key(b: np.ndarray) -> frozenset:
    return frozenset({tuple(b[0]), tuple(b[-1])})


def _public(rec: dict) -> dict:
    return {k: v for k, v in rec.items() if not k.startswith("_")}
