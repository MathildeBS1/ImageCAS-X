#!/usr/bin/env python
"""Apply Qiu et al. 2025 stage-2 reconnection to an existing run's predictions.

    python scripts/qiu_reconnect.py -c configs/cas_net_qiu.json \
        --src cas_net_pretrained -r cas_net_pretrained_qiu [--workers 8] [--overwrite]

Reads <results>/<src>/predictions/<id>.nii.gz for every test-split scan (or
<results>/<src>/predictions_<split>/<id>.nii.gz for --split val/train, matching
inference.py's own naming), writes the repaired mask to
<results>/<run>/predictions/<id>.nii.gz and a per-scan decision log to
<results>/<run>/reconnection_logs/<id>.json, then an aggregate
reconnection_summary.json. The output run dir is then scored like any other:

    python -m evaluate -c configs/cas_net_qiu.json -r cas_net_pretrained_qiu

The GT lumen is loaded for each scan only to annotate the log after every decision
is final (is each fragment real vessel, does each walked path lie in the lumen), which
is what reconnection_scores() turns into Qiu's RecAcc / RecSen / RecSpe. --no-gt skips
it. The decisions themselves never see GT.

Resumes by default: a scan with both its mask and its log already written is skipped.
A scan that raises is logged to reconnection_logs/<id>.error.txt and gets no
prediction, so evaluate.py reports it under coverage instead of silently scoring the
unrepaired mask in its place.
"""
import argparse
import json
import multiprocessing
import os
import subprocess
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postprocessing.qiu.reconnect import Reconnector, ReconnectParams  # noqa: E402
from utils import io as bio  # noqa: E402
from utils.config import BenchmarkConfig  # noqa: E402

_STATE = {}


def _resolve(root: str, run: str) -> str:
    return run if os.path.isabs(run) else os.path.join(root, run)


def _init_worker(params: dict, config_path: str, score_gt: bool):
    """The model is loaded once in the parent before the pool forks (_STATE["model"]),
    so workers share its tree arrays copy-on-write instead of each holding a copy."""
    import SimpleITK as sitk
    sitk.ProcessObject.SetGlobalDefaultNumberOfThreads(1)
    _STATE["reconnector"] = Reconnector(ReconnectParams.from_dict(params), _STATE.get("model"))
    _STATE["cfg"] = BenchmarkConfig.from_json(config_path) if score_gt else None


def _load_gt(scan_id: str, ref):
    """GT lumen on the prediction's grid, exactly as evaluate.py loads it."""
    from evaluate import _load_gt_labels
    cfg = _STATE["cfg"]
    return bio.binarise_lumen(_load_gt_labels(cfg, scan_id, ref))


def _process(scan_id: str, src_pred: str, out_pred: str, log_path: str, vol_path: str) -> tuple:
    try:
        pred, ref = bio.load_mask(src_pred)
        rec = _STATE["reconnector"]
        volume = np.load(vol_path, mmap_mode="r") if rec.p.mode == "qiu" else None
        gt = _load_gt(scan_id, ref) if _STATE["cfg"] is not None else None
        out, log = rec(pred, ref, None if volume is None else np.asarray(volume), gt=gt)
        log.update(scan_id=scan_id, voxels_added=int((out & ~pred.astype(bool)).sum()),
                   voxels_removed=int((pred.astype(bool) & ~out.astype(bool)).sum()))
        bio.save_mask(out, ref, out_pred)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=1, default=_jsonable)
        return scan_id, log, None
    except Exception:
        err = traceback.format_exc()
        with open(log_path.replace(".json", ".error.txt"), "w", encoding="utf-8") as f:
            f.write(err)
        return scan_id, None, err


def _jsonable(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def reconnection_scores(logs: list, true_fraction: float = 0.5, path_fraction: float = 0.8):
    """Qiu et al. eqs. 15-17, per fragment. A fragment is true vessel if at least
    `true_fraction` of it lies in the (1-voxel dilated) GT lumen. Attached + true + every
    accepted path through it at least `path_fraction` inside the GT lumen is a TP, any
    other attachment an FP; removed + not true is a TN, removed + true an FN.

    RecAcc = (TP + TN) / all,  RecSen = TP / (TP + FN),  RecSpe = TN / (TN + FP).
    Fragments kept unjoined (remove_unconnected false) are counted separately. None if
    the logs carry no GT annotation."""
    c = dict(tp=0, fp=0, tn=0, fn=0, kept_true=0, kept_false=0)
    for l in logs:
        accepted = [a for a in l.get("attempts_type1", []) + l.get("attempts", []) if a["accepted"]]
        for fr in l.get("fragments", []):
            if "gt_fraction" not in fr:
                return None
            true = fr["gt_fraction"] >= true_fraction
            if fr["decision"] == "attached":
                ok = all(a.get("path_in_gt_fraction", 0.0) >= path_fraction
                         for a in accepted if fr["label"] in a["labels"])
                c["tp" if (true and ok) else "fp"] += 1
            elif fr["decision"] == "removed":
                c["fn" if true else "tn"] += 1
            else:
                c["kept_true" if true else "kept_false"] += 1
    n = c["tp"] + c["fp"] + c["tn"] + c["fn"]
    div = lambda a, b: float(a / b) if b else float("nan")  # noqa: E731
    return dict(c, rec_acc=div(c["tp"] + c["tn"], n), rec_sen=div(c["tp"], c["tp"] + c["fn"]),
                rec_spe=div(c["tn"], c["tn"] + c["fp"]),
                true_fraction=true_fraction, path_fraction=path_fraction)


def _summarise(logs: list) -> dict:
    attempts = [a for l in logs for a in l.get("attempts_type1", []) + l.get("attempts", [])]
    by_type = {}
    for a in attempts:
        t = by_type.setdefault(str(a["type"]), dict(attempted=0, walk_reached=0, accepted=0))
        t["attempted"] += 1
        t["walk_reached"] += int(a["walk"] == "reached")
        t["accepted"] += int(a["accepted"])
    walk_fail = {}
    for a in attempts:
        if a["walk"] != "reached":
            walk_fail[a["walk"]] = walk_fail.get(a["walk"], 0) + 1
    b0b = np.array([l["b0_before"] for l in logs])
    b0a = np.array([l["b0_after"] for l in logs])
    return dict(
        n_scans=len(logs),
        b0_before_mean=float(b0b.mean()), b0_after_mean=float(b0a.mean()),
        scans_with_b0_2_before=int((b0b == 2).sum()), scans_with_b0_2_after=int((b0a == 2).sum()),
        fragments_total=int(sum(l.get("n_fragments", 0) for l in logs)),
        fragments_attached=int(sum(l.get("n_fragments_attached", 0) for l in logs)),
        fragments_removed=int(sum(l.get("n_fragments_removed", 0) for l in logs)),
        attempts_by_type=by_type, walk_failures=walk_fail,
        reconnection_vs_gt=reconnection_scores(logs),
        voxels_added=int(sum(l["voxels_added"] for l in logs)),
        voxels_removed=int(sum(l["voxels_removed"] for l in logs)),
        seconds_mean=float(np.mean([l["seconds"] for l in logs])),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=True)
    ap.add_argument("--src", required=True, help="Run dir holding the predictions to repair.")
    ap.add_argument("-r", "--results-dir", required=True, help="Output run dir.")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--split", default="test", choices=("train", "val", "test"))
    ap.add_argument("--ids", nargs="*", default=None, help="Only these scan ids.")
    ap.add_argument("--classifier", default=None,
                    help="model.joblib path; defaults to <results>/<centerline_classifier.dir>.")
    ap.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE",
                    help="Override reconnection params, e.g. --set eval_threshold=99 "
                         "(values parsed as JSON). Recorded in reconnection_config.json.")
    ap.add_argument("--no-gt", action="store_true",
                    help="Skip the post-hoc GT annotation of fragments and paths.")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        raw = json.load(f)
    params = dict(raw.get("reconnection", {}))
    for kv in args.set:
        k, v = kv.split("=", 1)
        params[k] = json.loads(v)
    ReconnectParams.from_dict(params)            # fail on a typo before any work
    cfg = BenchmarkConfig.from_json(args.config)
    src = _resolve(cfg.results_root, args.src)
    out = _resolve(cfg.results_root, args.results_dir)
    os.makedirs(os.path.join(out, "predictions"), exist_ok=True)
    os.makedirs(os.path.join(out, "reconnection_logs"), exist_ok=True)

    model_path = None
    if params.get("mode", "qiu") == "qiu":
        model_path = args.classifier or os.path.join(
            cfg.results_root, raw.get("centerline_classifier", {}).get("dir", "qiu_centerline_classifier"),
            "model.joblib")
        if not os.path.exists(model_path):
            sys.exit(f"Centerline classifier not found: {model_path}\n"
                     f"Train it first: bsub < jobs/train_qiu_classifier.sh")

    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True,
                                         cwd=os.path.dirname(os.path.abspath(__file__))).strip()
    except Exception:
        commit = "unknown"
    with open(os.path.join(out, "reconnection_config.json"), "w", encoding="utf-8") as f:
        json.dump(dict(config=os.path.abspath(args.config), source_run=src, split=args.split,
                       params=params, overrides=args.set, classifier=model_path,
                       git_commit=commit, started=time.strftime("%Y-%m-%d %H:%M:%S")), f, indent=2)

    ext = cfg.data.file_extension
    ids = args.ids or getattr(cfg.data, f"{args.split}_ids")
    # inference.py only writes the test split to predictions/; every other split goes to
    # predictions_<split>/ so val and test predictions never mix in the same run dir.
    src_pred_dir = "predictions" if args.split == "test" else f"predictions_{args.split}"
    jobs, logs, skipped_missing = [], [], []
    for sid in ids:
        src_pred = os.path.join(src, src_pred_dir, f"{sid}{ext}")
        out_pred = os.path.join(out, "predictions", f"{sid}{ext}")
        log_path = os.path.join(out, "reconnection_logs", f"{sid}.json")
        if not os.path.exists(src_pred):
            skipped_missing.append(sid)
            continue
        if not args.overwrite and os.path.exists(out_pred) and os.path.exists(log_path):
            with open(log_path, encoding="utf-8") as f:
                logs.append(json.load(f))
            continue
        vol_path = os.path.join(cfg.data.data_root, "volumes_resampled", f"{sid}.npy")
        jobs.append((sid, src_pred, out_pred, log_path, vol_path))
    print(f"[reconnect] {len(jobs)} to process, {len(logs)} already done, "
          f"{len(skipped_missing)} without a source prediction", flush=True)

    if model_path and jobs:
        import joblib
        _STATE["model"] = joblib.load(model_path).set_n_jobs(1)

    failed = []
    ctx = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx, initializer=_init_worker,
                             initargs=(params, os.path.abspath(args.config),
                                       not args.no_gt)) as pool:
        futures = [pool.submit(_process, *j) for j in jobs]
        for i, fut in enumerate(as_completed(futures), 1):
            sid, log, err = fut.result()
            if err:
                failed.append(sid)
                print(f"  [{i}/{len(jobs)}] {sid} FAILED: {err.strip().splitlines()[-1]}", flush=True)
            else:
                logs.append(log)
                print(f"  [{i}/{len(jobs)}] {sid}: b0 {log['b0_before']} -> {log['b0_after']}, "
                      f"+{log['voxels_added']} / -{log['voxels_removed']} vox, "
                      f"{log['seconds']:.0f}s", flush=True)

    summary = dict(_summarise(logs) if logs else {}, failed=sorted(failed),
                   missing_source=sorted(skipped_missing))
    with open(os.path.join(out, "reconnection_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
