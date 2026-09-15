"""The centerline classifier P of Qiu et al. eq. 7.

    P(A_k) = CFC( flat(maxpool(pat_big(A_k))) ++ flat(pat_small(A_k)) )

Two image patches centred on a voxel, the big one max-pooled down to the small one's
size, flattened and concatenated, fed to a cascade forest classifier (CFC). Final
setting per their Table 12: multiscale patch (15, 7), i.e. a 15^3 patch pooled to 7^3
plus a 7^3 patch, 686 features.

Qiu et al. use `CascadeForestClassifier` from the `deep-forest` package (Zhou & Feng
2019). That package ships no wheels for Python > 3.9, so `CascadeForest` below
rebuilds the same structure on scikit-learn: each layer is two random forests and two
extra-trees forests; each forest's out-of-bag class vector is appended to the raw
features for the next layer; layers stop being added when out-of-bag accuracy stops
improving. deep-forest's default histogram binning and its optional final predictor
are not reproduced.
"""
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier

BIG = 15
SMALL = 7


def normalise_hu(volume: np.ndarray, hu_min: float = -200.0, hu_max: float = 1000.0) -> np.ndarray:
    """The benchmark's own HU window (pipeline.json normalise_to_range) to [0, 1]."""
    v = np.clip(volume.astype(np.float32), hu_min, hu_max)
    return (v - hu_min) / (hu_max - hu_min)


def _offsets(size: int) -> np.ndarray:
    r = np.arange(size) - size // 2
    return np.stack(np.meshgrid(r, r, r, indexing="ij"), axis=-1).reshape(-1, 3)


_BIG_OFFSETS = _offsets(BIG)


def _maxpool_k3s2(p: np.ndarray) -> np.ndarray:
    """(K, 15, 15, 15) -> (K, 7, 7, 7), kernel 3 stride 2 on each spatial axis."""
    for ax in (1, 2, 3):
        n = p.shape[ax]
        a = np.take(p, np.arange(0, n - 2, 2), axis=ax)
        b = np.take(p, np.arange(1, n - 1, 2), axis=ax)
        c = np.take(p, np.arange(2, n, 2), axis=ax)
        p = np.maximum(np.maximum(a, b), c)
    return p


def patch_features(volume_norm: np.ndarray, points: np.ndarray, chunk: int = 2048) -> np.ndarray:
    """(K, 686) features for integer voxel `points` of a [0,1]-normalised volume.
    Coordinates past the border are clamped, i.e. the edge is replicated."""
    points = np.asarray(points, dtype=np.int64).reshape(-1, 3)
    hi = np.array(volume_norm.shape) - 1
    lo_s, hi_s = (BIG - SMALL) // 2, (BIG + SMALL) // 2
    out = []
    for s in range(0, len(points), chunk):
        idx = np.clip(points[s:s + chunk, None, :] + _BIG_OFFSETS[None], 0, hi)
        big = volume_norm[idx[..., 0], idx[..., 1], idx[..., 2]].reshape(-1, BIG, BIG, BIG)
        pooled = _maxpool_k3s2(big)
        small = big[:, lo_s:hi_s, lo_s:hi_s, lo_s:hi_s]
        out.append(np.concatenate([pooled.reshape(len(big), -1),
                                   small.reshape(len(big), -1)], axis=1))
    if not out:
        return np.zeros((0, 2 * SMALL ** 3), dtype=np.float32)
    return np.concatenate(out).astype(np.float32)


class CascadeForest:
    """Cascade forest (gcForest without multi-grained scanning) on scikit-learn."""

    def __init__(self, n_trees: int = 100, max_layers: int = 5, n_tolerant_rounds: int = 1,
                 delta: float = 1e-5, min_samples_leaf: int = 1, n_jobs: int = -1,
                 random_state: int = 42):
        self.n_trees = n_trees
        self.max_layers = max_layers
        self.n_tolerant_rounds = n_tolerant_rounds
        self.delta = delta
        self.min_samples_leaf = min_samples_leaf
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.layers = []
        self.layer_oob_accuracy = []

    def _make_layer(self, layer: int) -> list:
        kw = dict(n_estimators=self.n_trees, bootstrap=True, oob_score=True,
                  max_features="sqrt", min_samples_leaf=self.min_samples_leaf,
                  n_jobs=self.n_jobs)
        seed = self.random_state + 10 * layer
        return [RandomForestClassifier(random_state=seed, **kw),
                RandomForestClassifier(random_state=seed + 1, **kw),
                ExtraTreesClassifier(random_state=seed + 2, **kw),
                ExtraTreesClassifier(random_state=seed + 3, **kw)]

    def fit(self, X: np.ndarray, y: np.ndarray, verbose: bool = True) -> "CascadeForest":
        augment, best, best_n, tolerant = None, -np.inf, 0, 0
        self.layers, self.layer_oob_accuracy = [], []
        for layer in range(self.max_layers):
            Xl = X if augment is None else np.hstack([X, augment])
            forests = self._make_layer(layer)
            oob = []
            for f in forests:
                f.fit(Xl, y)
                oob.append(np.nan_to_num(f.oob_decision_function_, nan=0.5))
            acc = float(((np.mean(oob, axis=0)[:, 1] > 0.5).astype(int) == y).mean())
            self.layers.append(forests)
            self.layer_oob_accuracy.append(acc)
            if verbose:
                print(f"  [cascade] layer {layer + 1}: OOB accuracy {acc:.4f}", flush=True)
            if acc > best + self.delta:
                best, best_n, tolerant = acc, layer + 1, 0
            else:
                tolerant += 1
                if tolerant >= self.n_tolerant_rounds:
                    break
            augment = np.hstack(oob).astype(np.float32)
        self.layers = self.layers[:best_n]
        return self

    def set_n_jobs(self, n_jobs: int) -> "CascadeForest":
        for forests in self.layers:
            for f in forests:
                f.set_params(n_jobs=n_jobs)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        augment, probs = None, None
        for forests in self.layers:
            Xl = X if augment is None else np.hstack([X, augment])
            probs = [f.predict_proba(Xl) for f in forests]
            augment = np.hstack(probs).astype(np.float32)
        return np.mean(probs, axis=0)


class CenterlineProbability:
    """P(A) for voxels of one scan, cached: walks from neighbouring fragments revisit
    the same voxels, and the forest is the expensive part of every step."""

    def __init__(self, model: CascadeForest, volume_norm: np.ndarray):
        self.model = model
        self.volume = volume_norm
        self.cache = {}

    def __call__(self, points: np.ndarray) -> np.ndarray:
        points = np.asarray(points, dtype=np.int64).reshape(-1, 3)
        keys = [tuple(p) for p in points]
        todo = [i for i, k in enumerate(keys) if k not in self.cache]
        if todo:
            # Deduplicate before predicting; a batch can repeat a voxel.
            uniq = {keys[i]: i for i in todo}
            idx = list(uniq.values())
            p = self.model.predict_proba(patch_features(self.volume, points[idx]))[:, 1]
            for k, v in zip(uniq.keys(), p):
                self.cache[k] = float(v)
        return np.array([self.cache[k] for k in keys], dtype=np.float64)
