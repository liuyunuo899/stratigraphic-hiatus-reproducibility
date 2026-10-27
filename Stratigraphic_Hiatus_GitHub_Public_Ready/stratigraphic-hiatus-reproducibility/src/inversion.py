"""Identifiability experiment: how well does a final age-depth record constrain
the cumulative deposited mass?

Experiment design
-----------------
1. Take one synthetic truth (forcing class F3, fixed seed) -> preserved column.
2. Sample N=25 dated horizons from the preserved column with Gaussian age error
   (sigma_t = 2% of age) -> observations (t_i, z_i). Horizon thicknesses are
   measured; the dating uncertainty is propagated to an effective thickness
   uncertainty sigma_z = sigma_t * mean_rate (mean_rate = M_final / duration),
   which keeps the misfit functional dimensionally consistent.
3. Variational (Tikhonov) inversion: find smooth accumulation history r(t) >= 0
   minimising  J = sum_i ((z_model(t_i) - z_i)^2 / sigma_i^2) + lam * ||r''||^2.
   Solved as a linear-quadratic problem on a 100-node grid with non-negativity
   via NNLS on the smoothness-penalised system (scipy.optimize.nnls).
4. Identifiability ensemble: alternative depositional histories consistent with
   the same observations are constructed by inserting, within each preserved-
   record gap, episodes of deposition followed by complete erosion. For each
   gap, the removed thickness is drawn from an exponential distribution whose
   mean is gap_duration * mean_rate_obs (mean_rate_obs estimated from the
   inverted smooth history). 5000 realisations, fixed seed.
Outputs: data/synthetic/inversion_*.csv / .npz
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
from scipy.optimize import nnls
from simulation import run_column

SYN = str(ROOT / "data/synthetic")
SEED = 20261020


def build_truth():
    r = run_column("F3", SEED + 777)
    layers = r["layers"]
    # age-depth path of the PRESERVED column: cumulative preserved thickness vs depositional time
    ages, depths = [0.0], [0.0]
    cum = 0.0
    for t0, t1, th in layers:
        ages += [t0, t1]
        depths += [cum, cum + th]
        cum += th
    return np.array(ages), np.array(depths), r


def sample_observations(ages, depths, n=25, rng=None):
    rng = rng or np.random.default_rng(SEED)
    t_max = ages[-1]
    ts = np.sort(rng.uniform(ages[0], t_max, n))
    sig_t = 0.02 * np.maximum(ts, 0.05)
    t_obs = ts + rng.normal(0, sig_t)
    order = np.argsort(t_obs)
    t_obs = t_obs[order]
    z_obs = np.interp(t_obs, ages, depths)
    # propagate dating error to thickness units via the mean accumulation rate
    mean_rate = depths[-1] / ages[-1]
    sig_z = np.maximum(sig_t[order] * mean_rate, 0.05)
    return t_obs, z_obs, sig_t[order], sig_z


def tikhonov_invert(t_obs, z_obs, sig, lam, n_grid=100, t_max=None):
    t_max = t_max or t_obs.max() * 1.02
    tg = np.linspace(0, t_max, n_grid)
    # model: z(t) = cumulative sum of r * dt  -> linear operator A (n_obs x n_grid)
    dtg = tg[1] - tg[0]
    A = np.zeros((len(t_obs), n_grid))
    for i, t in enumerate(t_obs):
        A[i] = (tg <= t) * dtg
    A /= sig[:, None]
    # second-difference smoothness
    D = np.diff(np.eye(n_grid), 2, axis=0)
    M = np.vstack([A, np.sqrt(lam) * D])
    b = np.concatenate([z_obs / sig, np.zeros(n_grid - 2)])
    r, _ = nnls(M, b)
    return tg, r


def identifiability_ensemble(ages, depths, mean_rate, n_mc=5000, seed=SEED + 99):
    """Insert deposit-then-erode episodes into record gaps."""
    rng = np.random.default_rng(seed)
    gaps = []
    prev_t1 = ages[0]
    for k in range(1, len(ages), 2):
        t0, t1 = ages[k], ages[k + 1]
        if t0 > prev_t1:
            gaps.append(t0 - prev_t1)
        prev_t1 = t1
    gaps = np.array([g for g in gaps if g > 0])
    M_final = depths[-1]
    out = []
    for _ in range(n_mc):
        extra = 0.0
        for g in gaps:
            lam = max(g * mean_rate, 1e-6)
            if rng.uniform() < 0.7:  # probability that the gap hides an eroded episode
                extra += rng.exponential(lam)
        M_gross = M_final + extra
        out.append(M_gross)
    out = np.array(out)
    return pd.DataFrame(dict(M_gross=out, P=M_final / out)), gaps, M_final


def main():
    ages, depths, truth = build_truth()
    print("truth: M_gross=%.1f m, M_final=%.1f m, P=%.3f" % (truth["M_gross"], truth["M_final"], truth["P"]))
    t_obs, z_obs, sig_t, sig_z = sample_observations(ages, depths)
    pd.DataFrame(dict(t_obs=t_obs, z_obs=z_obs, sigma_t=sig_t,
                      sigma_z=sig_z)).to_csv(f"{SYN}/inversion_observations.csv", index=False)
    curves = []
    for lam in [0.1, 1, 10, 100]:
        tg, r = tikhonov_invert(t_obs, z_obs, sig_z, lam)
        for a, b in zip(tg, r):
            curves.append(dict(lam=lam, t=a, rate=b))
    pd.DataFrame(curves).to_csv(f"{SYN}/inversion_curves.csv", index=False)
    mean_rate = z_obs[-1] / t_obs[-1]
    ens, gaps, M_final = identifiability_ensemble(ages, depths, mean_rate)
    ens.to_csv(f"{SYN}/inversion_ensemble.csv", index=False)
    print("gaps used:", len(gaps), "| M_final=%.1f m" % M_final)
    print("M_gross: median %.1f, 95%% interval [%.1f, %.1f]" %
          (ens["M_gross"].median(), ens["M_gross"].quantile(0.025), ens["M_gross"].quantile(0.975)))
    print("P: median %.3f, 95%% interval [%.3f, %.3f]" %
          (ens["P"].median(), ens["P"].quantile(0.025), ens["P"].quantile(0.975)))


if __name__ == "__main__":
    main()
