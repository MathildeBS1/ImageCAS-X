"""Geometry parameter budget for the segment-level cloglog GLMM (who question).

OWN CALCULATION on aggregate numbers and SYNTHETIC data only. No individual CGPS data are used.
Aggregate inputs (all from project files):
  - 1,076 people with an outcome, 452 (42.0 %) developed trunk plaque; 1,041 complete cases,
    433 (41.6 %) events                                  [CGPS_data/score2_honesty.md]
  - OOF log-loss of the SCORE2-recalibrated base 0.6284, refitted factors 0.6346; OOF C 0.687 / 0.686
                                                          [CGPS_data/score2_honesty.md]
  - HR per SD of the refitted factors (person-level cloglog) [CGPS_data/score2_honesty.md]
  - 2.45 trunk plaque segments per affected person (1,534 / 626, OLD 1,352-person table)
    and artery shares LAD 846, CX 260, RCA 428            [CGPS_data/plaque_location.md]
Base design as in CGPS_data/progression_who_pooled.py design(): intercept, log follow-up,
SCORE2 (1 df) or factors (age, sbp, tc, hdl per SD + male + current smoking = 6 df), right
dominance, 8 segment dummies, log length (+ random-intercept SD).

Run:  python3 budget_sim.py [--reps 40] [--quick]
numpy + scipy only.
"""
import argparse
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np
from scipy import optimize, stats
from scipy.special import expit, logit, logsumexp

OUT = os.path.dirname(os.path.abspath(__file__))
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ============================================================ 1. Riley criteria (person level)
def r2cs_from_c(C, phi, nodes=200):
    """Binormal conversion (Riley, Van Calster & Collins 2021, Stat Med 40:859):
    LP ~ N(mu,1) in events, N(0,1) in non-events, mu = sqrt(2) * Phi^-1(C); fit a logistic model
    of y on LP to the (infinite) population, R2_CS = 1 - exp(-LR/n). Done here by quadrature
    (expected log-likelihood per person) instead of a 1e6-row simulation."""
    mu = np.sqrt(2) * stats.norm.ppf(C)
    x, w = np.polynomial.hermite_e.hermegauss(nodes)
    w = w / w.sum()
    lp1, lp0 = x + mu, x

    def nll(t):
        a, b = t
        return -(phi * np.sum(w * np.log(expit(a + b * lp1)))
                 + (1 - phi) * np.sum(w * np.log(expit(-(a + b * lp0)))))

    res = optimize.minimize(nll, [logit(phi), 1.0], method="Nelder-Mead",
                            options=dict(xatol=1e-10, fatol=1e-13, maxiter=5000))
    l_null = phi * np.log(phi) + (1 - phi) * np.log(1 - phi)
    return 1 - np.exp(-2 * (-res.fun - l_null))


def r2cs_max(phi):
    l_null = phi * np.log(phi) + (1 - phi) * np.log(1 - phi)
    return 1 - np.exp(2 * l_null)


def pmax_shrink(n, r2, S=0.9):
    """Riley criterion (i) solved for P:  n = P / ((S-1) ln(1 - R2/S))."""
    return n * (S - 1) * np.log(1 - r2 / S)


def pmax_optimism(n, r2, phi, delta=0.05):
    """Criterion (ii): S_VH = R2 / (R2 + delta * R2max), then as (i) with that S."""
    S = r2 / (r2 + delta * r2cs_max(phi))
    return pmax_shrink(n, r2, S), S


def riley_section():
    say("\n# 1. Riley criteria at person level (own calculation)")
    rows = []
    for n, ev in ((1076, 452), (1041, 433)):
        phi = ev / n
        mx = r2cs_max(phi)
        say(f"\nn = {n}, events = {ev}, phi = {phi:.4f}; max R2_CS = {mx:.4f}; "
            f"criterion (iii) needs n >= {(1.96 / 0.05) ** 2 * phi * (1 - phi):.0f} (met)")
        # anchor from the observed OOF log-loss of the bases (aggregate)
        l_null = -(phi * np.log(phi) + (1 - phi) * np.log(1 - phi))
        for name, ll in (("SCORE2 recalibrated, OOF log-loss 0.6284", 0.6284),
                         ("refitted factors, OOF log-loss 0.6346", 0.6346)):
            r2 = 1 - np.exp(-2 * (l_null - ll))
            say(f"  anchor: {name}: OOF R2_CS = {r2:.4f} (null log-loss {l_null:.4f})")
        say("| C | R2_CS | P_max crit (i) S=0.9 | S_VH crit (ii) | P_max crit (ii) | binding P_max |")
        say("|---|---|---|---|---|---|")
        cases = [(c, r2cs_from_c(c, phi)) for c in (0.65, 0.70, 0.72, 0.75)]
        cases.append(("15% of max", 0.15 * mx))
        for c, r2 in cases:
            p1 = pmax_shrink(n, r2)
            p2, s2 = pmax_optimism(n, r2, phi)
            pb = min(p1, p2)
            say(f"| {c} | {r2:.4f} | {p1:.1f} | {s2:.3f} | {p2:.1f} | {pb:.1f} |")
            rows.append(dict(n=n, C=str(c), r2=r2, p_i=p1, p_ii=p2, s_ii=s2, binding=pb))
    return rows


# ============================================================ synthetic design
SEGS = ["pLAD", "mLAD", "dLAD", "pCX", "mCX", "dCX", "pRCA", "mRCA", "dRCA"]
# event share: artery shares from plaque_location.md (846/260/428 of 1,534); p/m/d split ASSUMED
SHARE = np.r_[0.551 * np.r_[.40, .40, .20], 0.170 * np.r_[.45, .30, .25], 0.279 * np.r_[.40, .35, .25]]
LEN_MM = np.r_[20, 30, 35, 15, 15, 20, 25, 30, 25.]  # ASSUMED typical segment lengths
GAMMA_LEN = 0.5                                       # ASSUMED log-length coefficient
# refitted-factor log HR per SD, from score2_honesty.md (person-level, marginal):
# age, sbp, tc, hdl, male, smoking ; log follow-up
W_FACT = np.log(np.r_[1.32, 1.22, 1.09, 0.86, 1.25, 1.14])
W_FU = np.log(1.19)
# a SCORE2-like proxy: different weights (age-heavy), plus noise for the nonlinear terms (ASSUMED)
W_S2 = np.r_[0.50, 0.15, 0.10, -0.10, 0.20, 0.20]
GEO_LOGHR_MAIN = np.log(np.r_[1.20, 1.15, 1.15, 1.10, 1.10])  # curvature, LM angle, taper, LM->LAD, LM->LCx
GEO_TYPE_MAIN = ["seg", "per", "seg", "per", "per"]
KMAX = 12


def geo_spec(extra_hr):
    types = GEO_TYPE_MAIN + ["seg" if j % 2 == 0 else "per" for j in range(KMAX - 5)]
    lhr = np.r_[GEO_LOGHR_MAIN, np.full(KMAX - 5, np.log(extra_hr))]
    return types, lhr


def gen(N, truth, rng):
    """One synthetic cohort, rows sorted by person (9 rows each)."""
    J = len(SEGS)
    # person factors: age, sbp, tc, hdl continuous (age-sbp corr 0.3, tc-hdl corr 0.2), male, smoking binary
    z = rng.standard_normal((N, 4))
    z[:, 1] = 0.3 * z[:, 0] + np.sqrt(1 - .09) * z[:, 1]
    z[:, 3] = 0.2 * z[:, 2] + np.sqrt(1 - .04) * z[:, 3]
    male = (rng.random(N) < 0.45).astype(float)
    smk = (rng.random(N) < 0.12).astype(float)
    F = np.column_stack([z, (male - .45) / np.sqrt(.45 * .55), (smk - .12) / np.sqrt(.12 * .88)])
    fu = rng.standard_normal(N)
    s2 = F @ W_S2 + 0.35 * rng.standard_normal(N)
    s2 = (s2 - s2.mean()) / s2.std()
    right = (rng.random(N) < 0.88).astype(float)
    # segment rows
    seg = np.tile(np.arange(J), N)
    pid = np.repeat(np.arange(N), J)
    loglen = (np.log(LEN_MM)[seg] + 0.15 * rng.standard_normal(N)[pid]
              + 0.25 * rng.standard_normal(N * J))
    types, lhr = truth["types"], truth["lhr"]
    G = np.empty((N * J, KMAX))
    for k, t in enumerate(types):
        if t == "seg":  # curvature/taper-like: within-type z-score, 30 % between-person variance
            G[:, k] = np.sqrt(.3) * rng.standard_normal(N)[pid] + np.sqrt(.7) * rng.standard_normal(N * J)
        else:          # LM angle / ratios: person-level, mildly correlated with age (r = 0.2)
            G[:, k] = (0.2 * z[:, 0] + np.sqrt(.96) * rng.standard_normal(N))[pid]
    alpha = np.log(SHARE) - GAMMA_LEN * np.log(LEN_MM) + truth["a0"]
    eta = (alpha[seg] + GAMMA_LEN * loglen + truth["c"] * (F @ W_FACT)[pid] + W_FU * fu[pid]
           + G @ lhr)
    b = truth["sigma"] * rng.standard_normal(N)
    p = -np.expm1(-np.exp(eta + b[pid]))
    y = (rng.random(N * J) < p).astype(float)
    return dict(N=N, pid=pid, seg=seg, F=F, fu=fu, s2=s2, right=right, loglen=loglen, G=G, y=y,
                eta=eta)


def design(d, base, k):
    pid, seg = d["pid"], d["seg"]
    cols = [np.ones(len(seg)), d["fu"][pid]]
    if base == "refit":
        cols += [d["F"][pid, j] for j in range(6)]
    else:
        cols.append(d["s2"][pid])
    cols.append(d["right"][pid])
    cols += [(seg == s).astype(float) for s in range(1, len(SEGS))]  # pLAD reference
    cols.append(d["loglen"])
    if k:
        cols += [d["G"][:, j] for j in range(k)]
    return np.column_stack(cols)


# ============================================================ cloglog GLMM, own implementation
def nll(theta, X, y, starts, rp, xq, logw):
    beta, ls = theta[:-1], theta[-1]
    u = np.sqrt(2.0) * np.exp(ls) * xq
    eta = np.clip((X @ beta)[:, None] + u[None], -30, 30)
    mu = np.exp(eta)
    one = y[:, None] == 1
    lij = np.where(one, np.log(-np.expm1(-mu)), -mu)
    a = np.add.reduceat(lij, starts, axis=0) + logw[None]
    lse = logsumexp(a, axis=1)
    r = np.exp(a - lse[:, None])[rp]
    g = np.where(one, mu * np.exp(-mu) / np.maximum(-np.expm1(-mu), 1e-300), -mu)
    rg = r * g
    grad = np.r_[X.T @ rg.sum(1), (rg * u[None]).sum()]
    return -lse.sum(), -grad


def fit(X, y, pid, theta0=None, nodes=20):
    starts = np.flatnonzero(np.r_[True, pid[1:] != pid[:-1]])
    xq, wq = np.polynomial.hermite.hermgauss(nodes)
    args = (X, y, starts, pid, xq, np.log(wq / np.sqrt(np.pi)))
    if theta0 is None:
        theta0 = np.zeros(X.shape[1] + 1)
        theta0[0] = np.log(-np.log(1 - y.mean()))
        theta0[-1] = np.log(0.5)
    r = optimize.minimize(nll, theta0, args=args, jac=True, method="L-BFGS-B",
                          options=dict(maxiter=2000, gtol=1e-6))
    return r.x, -r.fun, r.success


def person_risk(X, beta, sigma, pid, N, nodes=40):
    """P(any trunk plaque) = int 1 - exp(-e^b sum_j e^eta_ij) phi(b) db (cumulative hazards add)."""
    S = np.bincount(pid, weights=np.exp(X @ beta), minlength=N)
    xq, wq = np.polynomial.hermite.hermgauss(nodes)
    eb = np.exp(np.sqrt(2) * sigma * xq)
    return np.clip((wq / np.sqrt(np.pi) * -np.expm1(-S[:, None] * eb[None])).sum(1), 1e-9, 1 - 1e-9)


def cstat(p, y):
    r = stats.rankdata(p)
    n1 = y.sum()
    n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def cal_slope(p, y):
    lp = logit(p)
    Z = np.column_stack([np.ones_like(lp), lp])
    t = np.zeros(2)
    for _ in range(50):
        m = expit(Z @ t)
        H = Z.T @ (Z * (m * (1 - m))[:, None])
        step = np.linalg.solve(H, Z.T @ (y - m))
        t += step
        if np.abs(step).max() < 1e-10:
            break
    # calibration-in-the-large: intercept with slope fixed at 1 (offset)
    a = 0.0
    for _ in range(50):
        m = expit(a + lp)
        step = (y - m).sum() / (m * (1 - m)).sum()
        a += step
        if abs(step) < 1e-12:
            break
    return t[1], a


def true_person_risk(d, truth, geo=True):
    eta = d["eta"] if geo else d["eta"] - d["G"] @ truth["lhr"]
    S = np.bincount(d["pid"], weights=np.exp(eta), minlength=d["N"])
    xq, wq = np.polynomial.hermite.hermgauss(40)
    eb = np.exp(np.sqrt(2) * truth["sigma"] * xq)
    return (wq / np.sqrt(np.pi) * -np.expm1(-S[:, None] * eb[None])).sum(1)


def person_y(d):
    return (np.bincount(d["pid"], weights=d["y"], minlength=d["N"]) > 0).astype(float)


def calibrate_truth(icc, extra_hr, rng, target_prev=0.42, target_c_base=0.70, N=40000):
    """Pick factor multiplier c (base C) and a0 (prevalence 42 %) for a latent ICC."""
    sigma = np.sqrt(icc / (1 - icc) * np.pi ** 2 / 6)
    types, lhr = geo_spec(extra_hr)
    truth = dict(sigma=sigma, types=types, lhr=lhr, a0=0.0, c=1.0)
    seed = rng.integers(1 << 31)
    for _ in range(4):
        def prev_gap(a0):
            truth["a0"] = a0
            return true_person_risk(gen(N, truth, np.random.default_rng(seed)), truth).mean() - target_prev
        truth["a0"] = optimize.brentq(prev_gap, -12, 6, xtol=1e-4)

        def c_gap(c):
            truth["c"] = c
            d = gen(N, truth, np.random.default_rng(seed))
            p = true_person_risk(d, truth, geo=False)
            return cstat(p, person_y(d)) - target_c_base
        truth["c"] = optimize.brentq(c_gap, 0.2, 6.0, xtol=1e-3)
    truth["a0"] = optimize.brentq(prev_gap, -12, 6, xtol=1e-4)
    return truth


def describe_truth(truth, rng, N=100000):
    d = gen(N, truth, rng)
    yp = person_y(d)
    cnt = np.bincount(d["pid"], weights=d["y"], minlength=N)
    J = len(SEGS)
    q = d["y"].mean()
    # observed-scale within-person correlation of segment outcomes and design effect
    var_cnt = cnt.var()
    rho_obs = (var_cnt / (J * q * (1 - q)) - 1) / (J - 1)
    seg_share = np.bincount(d["seg"], weights=d["y"]) / d["y"].sum()
    return dict(prev=yp.mean(), seg_events_per_1076=d["y"].sum() / N * 1076,
                seg_per_affected=cnt[yp == 1].mean(), rho_obs=rho_obs,
                deff=1 + (J - 1) * rho_obs, q_seg=q,
                c_true_base=cstat(true_person_risk(d, truth, geo=False), yp),
                c_true_full=cstat(true_person_risk(d, truth), yp),
                seg_share=seg_share.round(3).tolist())


# ============================================================ one replicate
KS = [0, 2, 4, 5, 6, 7, 8, 10, 12]


def replicate(args):
    seed, truth, base, val = args
    rng = np.random.default_rng(seed)
    d = gen(1076, truth, rng)
    out = {}
    # null model (intercept + sigma) for heuristic shrinkage
    X0 = np.ones((len(d["y"]), 1))
    _, l_null, _ = fit(X0, d["y"], d["pid"])
    theta_prev = None
    l_base = None
    yv = person_y(val)
    for k in KS:
        X = design(d, base, k)
        th0 = None
        if theta_prev is not None:
            th0 = np.r_[theta_prev[:-1], np.zeros(X.shape[1] + 1 - len(theta_prev)), theta_prev[-1]]
        th, ll, ok = fit(X, d["y"], d["pid"], th0)
        theta_prev = th
        if k == 0:
            l_base = ll
        Xv = design(val, base, k)
        pv = person_risk(Xv, th[:-1], np.exp(th[-1]), val["pid"], val["N"])
        slope, citl = cal_slope(pv, yv)
        p = X.shape[1] - 1
        lr_all = 2 * (ll - l_null)
        out[k] = dict(slope=slope, citl=citl, c=cstat(pv, yv), lr_geo=2 * (ll - l_base),
                      s_vh=1 - p / lr_all, sigma=np.exp(th[-1]), ok=ok, p=p)
    return out


def summarise(res, truth_desc, label):
    say(f"\n### {label}")
    say(f"truth: {json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in truth_desc.items()})}")
    say("| k geo df | total fixed df (excl. intercept) | mean OOS calibration slope (MC SE) | P(slope<0.9) | "
        "mean heuristic S_VH | OOS C | CITL | LR-test power (alpha 0.05) | mean sigma-hat | non-converged |")
    say("|---|---|---|---|---|---|---|---|---|---|")
    rows = {}
    for k in KS:
        sl = np.array([r[k]["slope"] for r in res])
        sv = np.array([r[k]["s_vh"] for r in res])
        cc = np.array([r[k]["c"] for r in res])
        ci = np.array([r[k]["citl"] for r in res])
        lr = np.array([r[k]["lr_geo"] for r in res])
        sg = np.array([r[k]["sigma"] for r in res])
        bad = sum(not r[k]["ok"] for r in res)
        pw = np.mean(lr > stats.chi2.ppf(.95, k)) if k else np.nan
        rows[k] = dict(slope=sl.mean(), slope_se=sl.std(ddof=1) / np.sqrt(len(sl)), svh=sv.mean(),
                       c=cc.mean(), power=pw, lr_mean=lr.mean(), p=res[0][k]["p"])
        say(f"| {k} | {res[0][k]['p']} | {sl.mean():.3f} ({sl.std(ddof=1) / np.sqrt(len(sl)):.3f}) | "
            f"{np.mean(sl < .9):.2f} | {sv.mean():.3f} | {cc.mean():.4f} | {ci.mean():+.3f} | "
            f"{'' if k == 0 else f'{pw:.2f}'} | {sg.mean():.3f} | {bad} |")
    below = [k for k in KS if rows[k]["slope"] < 0.9]
    say(f"first k with mean slope < 0.9: {below[0] if below else 'none up to 12'}")
    return rows


# ============================================================ 4. power under fixed total signal
def power_section(lam_list):
    say("\n# 4. Power of the k-df LR test at a FIXED noncentrality (same total signal spread over k df)")
    say("| noncentrality | " + " | ".join(f"k={k}" for k in (1, 2, 3, 5, 7, 9, 12)) + " |")
    say("|---|" + "---|" * 7)
    for lam in lam_list:
        pw = [stats.ncx2.sf(stats.chi2.ppf(.95, k), k, lam) for k in (1, 2, 3, 5, 7, 9, 12)]
        say(f"| {lam:.1f} | " + " | ".join(f"{p:.2f}" for p in pw) + " |")


# ============================================================ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=40)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--nval", type=int, default=20000)
    a = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(20261102)
    say("OWN CALCULATION. Aggregate inputs + synthetic data only; no individual data.")
    riley = riley_section()

    # 2. Harrell + design effect, using the generator's observed-scale correlation
    say("\n# 2/3. Synthetic truths (latent ICC -> observed-scale design effect) and simulation")
    scen = [(0.1, 1.0), (0.3, 1.0), (0.55, 1.0), (0.55, 1.10)] if not a.quick else [(0.2, 1.0)]
    allres = {}
    harrell = []
    for icc, extra in scen:
        truth = calibrate_truth(icc, extra, rng)
        desc = describe_truth(truth, np.random.default_rng(rng.integers(1 << 31)))
        desc.update(icc_latent=icc, sigma=truth["sigma"], c_mult=truth["c"], extra_hr=extra)
        if extra == 1.0:
            E = 452 * 2.45
            n = 1076 * 9
            q = E / n
            for mname, m in (("min(events, non-events)", min(E, n - E)), ("3nq(1-q) [ordinal formula]", 3 * n * q * (1 - q))):
                harrell.append((icc, desc["rho_obs"], desc["deff"], mname, m, m / desc["deff"] / 15,
                                desc["seg_events_per_1076"], desc["seg_per_affected"]))
        val = gen(a.nval, truth, np.random.default_rng(rng.integers(1 << 31)))
        for base in ("recal", "refit"):
            seeds = rng.integers(1 << 31, size=a.reps)
            with Pool(min(8, os.cpu_count())) as pool:
                res = pool.map(replicate, [(int(s), truth, base, val) for s in seeds])
            label = (f"latent ICC {icc}, extra geometry HR {extra} ({'null extras' if extra == 1 else 'all features carry signal'}), "
                     f"base = {'SCORE2 recalibrated' if base == 'recal' else 'refitted factors (6)'}; {a.reps} reps")
            allres[(icc, extra, base)] = summarise(res, desc, label)
            say(f"[elapsed {time.time() - t0:.0f}s]")

    say("\n# 2. Harrell m/15 at segment level with design effect (own calculation)")
    say("Segment events ESTIMATED: 452 x 2.45 = 1,107 (2.45 from the OLD 1,352-person table); rows 1,076 x 9 = 9,684.")
    say("| latent ICC | observed-scale rho (synthetic) | design effect | m definition | m | df = m/(DE*15) | synthetic seg events per 1,076 | synthetic seg per affected |")
    say("|---|---|---|---|---|---|---|---|")
    for h in harrell:
        say(f"| {h[0]} | {h[1]:.3f} | {h[2]:.2f} | {h[3]} | {h[4]:.0f} | {h[5]:.0f} | {h[6]:.0f} | {h[7]:.2f} |")

    lam5 = [allres[k][5]["lr_mean"] - 5 for k in allres if k[1] == 1.0]
    power_section(sorted(set([round(x, 1) for x in lam5] + [5.0, 10.0, 15.0, 20.0, 30.0])))

    # 5. final table
    say("\n# 5. Geometry df affordable (Riley binding P_max minus base df; n = 1,076)")
    base_df = {"SCORE2 recalibrated": 12, "refitted factors (6)": 17, "refitted factors + diabetes": 18}
    say("Base df (excl. intercept): log FU 1 + SCORE2 1 | factors 6(+1) + dominance 1 + 8 segment dummies + log length 1."
        " The random-intercept SD would add 1 more if counted.")
    say("| base | C | P_max (binding) | base df | geometry df left | 5 (no Mundlak) fits? | 7 (Mundlak) fits? |")
    say("|---|---|---|---|---|---|---|")
    for bname, bd in base_df.items():
        for r in riley:
            if r["n"] != 1076:
                continue
            left = r["binding"] - bd
            say(f"| {bname} | {r['C']} | {r['binding']:.1f} | {bd} | {left:.1f} | {'yes' if left >= 5 else 'no'} | {'yes' if left >= 7 else 'no'} |")
    say("\nSimulation (person-level OOS calibration slope of aggregated risk), first k with mean slope < 0.9:")
    for key, rows in allres.items():
        below = [k for k in KS if rows[k]["slope"] < 0.9]
        say(f"  ICC {key[0]}, extra HR {key[1]}, base {key[2]}: {below[0] if below else '>12'}; "
            f"slope at k=5: {rows[5]['slope']:.3f}, k=7: {rows[7]['slope']:.3f}, k=12: {rows[12]['slope']:.3f}")
    say(f"\nTotal runtime {time.time() - t0:.0f}s")
    with open(os.path.join(OUT, "budget_sim_output.md" if not a.quick else "budget_sim_quick.md"), "w") as f:
        f.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
