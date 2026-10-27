"""Case II: controlled synthetic deposition-erosion-stasis experiments.

Model (1-D surface elevation z(t), discrete time)
-------------------------------------------------
- dt = 0.5 kyr, T = 5 Myr (10,000 steps) unless stated otherwise.
- Environmental driver u(t), three forcing classes:
    F1 white-noise: u ~ N(0, 1), i.i.d.
    F2 multi-periodic: sum of sinusoids at 40/100/400/1200 kyr + white noise
    F3 long-memory: cumulative sum of white noise (Brownian) + white noise
- Switching: deposition at rate v_d when u > theta_d; erosion at rate v_e when
  u < -theta_e; otherwise stasis. Erosion cannot cut below z = 0 (basement).
- Layer tracking: each depositional increment is a labelled layer
  (t_start, t_end, thickness); erosion peels layers from the top (LIFO).
- Outputs per run: hiatus durations in the final record (gaps between preserved
  depositional intervals), completeness at resolution tau, gross deposited
  thickness M_gross, final preserved thickness M_final, preservation efficiency
  P = M_final / M_gross.
Randomness: numpy default_rng; master seed 20261020, run seeds master+i.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd

SYN = str(ROOT / "data/synthetic")
MASTER_SEED = 20261020
TAUS = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]  # Myr
PERIODS_KYR = [40, 100, 400, 1200]  # Milankovitch-like + grand-cycle band


def make_driver(kind, n, dt_kyr, rng, noise_amp=0.5):
    t = np.arange(n) * dt_kyr
    if kind == "F1":
        u = rng.standard_normal(n)
    elif kind == "F2":
        u = sum(np.sin(2 * np.pi * t / p + rng.uniform(0, 2 * np.pi)) for p in PERIODS_KYR)
        u = u / np.std(u) + noise_amp * rng.standard_normal(n)
    elif kind == "F3":
        u = np.cumsum(rng.standard_normal(n))
        u = u / np.std(u) + noise_amp * rng.standard_normal(n)
    else:
        raise ValueError(kind)
    return (u - u.mean()) / u.std()


def run_column(kind, seed, T_myr=5.0, dt_kyr=0.5, v_d=0.2, v_e=0.2,
               theta_d=0.5, theta_e=0.5, noise_amp=0.5):
    """Simulate one column. v_d, v_e in m/kyr; returns dict of results."""
    rng = np.random.default_rng(seed)
    n = int(T_myr * 1000 / dt_kyr)
    u = make_driver(kind, n, dt_kyr, rng, noise_amp)
    z = 0.0
    layers = []          # preserved layers: [t_start_myr, t_end_myr, thickness_m]
    gross = 0.0
    open_layer = None    # currently accumulating layer
    for i in range(n):
        t0 = i * dt_kyr / 1000.0
        if u[i] > theta_d:
            dz = v_d * dt_kyr
            z += dz; gross += dz
            if open_layer is None:
                open_layer = [t0, t0, dz]
            else:
                open_layer[1] = t0; open_layer[2] += dz
        elif u[i] < -theta_e:
            dz = min(v_e * dt_kyr, z)
            z -= dz
            rem = dz
            while rem > 1e-12 and layers:
                top = layers[-1]
                take = min(top[2], rem)
                top[2] -= take; rem -= take
                if top[2] <= 1e-12:
                    layers.pop()
            if open_layer is not None:
                take = min(open_layer[2], rem)
                open_layer[2] -= take; rem -= take
                if open_layer[2] <= 1e-12:
                    open_layer = None
            if open_layer is not None:
                layers.append(open_layer); open_layer = None
        else:
            if open_layer is not None:
                layers.append(open_layer); open_layer = None
    if open_layer is not None:
        layers.append(open_layer)
    layers = [l for l in layers if l[2] > 1e-9]
    final = sum(l[2] for l in layers)
    # hiatuses in the final record
    hiatuses = [layers[i + 1][0] - layers[i][1] for i in range(len(layers) - 1)]
    hiatuses = np.array([h for h in hiatuses if h > 0])
    # completeness at resolution tau
    comp = {}
    for tau in TAUS:
        nb = int(T_myr / tau)
        covered = np.zeros(nb, dtype=bool)
        for t0, t1, th in layers:
            i0 = int(t0 // tau); i1 = min(int(t1 // tau), nb - 1)
            covered[i0:i1 + 1] = True
        comp[tau] = covered.mean()
    return dict(kind=kind, hiatuses=hiatuses, completeness=comp,
                M_gross=gross, M_final=final, P=(final / gross if gross > 0 else np.nan),
                n_layers=len(layers), layers=layers)


def ensemble(kind, n_runs=200, **kw):
    rows, hiats = [], []
    for i in range(n_runs):
        r = run_column(kind, MASTER_SEED + i, **kw)
        rows.append(dict(kind=kind, run=i, M_gross=r["M_gross"], M_final=r["M_final"],
                         P=r["P"], n_layers=r["n_layers"],
                         **{f"C_{tau}": r["completeness"][tau] for tau in TAUS}))
        for h in r["hiatuses"]:
            hiats.append(dict(kind=kind, run=i, hiatus_myr=h))
    return pd.DataFrame(rows), pd.DataFrame(hiats)


def main():
    all_runs, all_hiats = [], []
    for kind in ["F1", "F2", "F3"]:
        df_r, df_h = ensemble(kind)
        all_runs.append(df_r); all_hiats.append(df_h)
        print(kind, "P median:", np.nanmedian(df_r["P"]).round(3),
              "| hiatuses:", len(df_h), "| median h:", np.median(df_h["hiatus_myr"]).round(4))
    # sensitivity sweeps
    sweep_rows = []
    for theta in [0.25, 0.5, 0.75, 1.0]:
        for ve_vd in [0.5, 1.0, 2.0]:
            for kind in ["F1", "F2", "F3"]:
                rows = []
                for i in range(50):
                    r = run_column(kind, MASTER_SEED + 10000 + i,
                                   theta_d=theta, theta_e=theta, v_d=0.2, v_e=0.2 * ve_vd)
                    rows.append((r["P"], len(r["hiatuses"])))
                arr = np.array(rows)
                sweep_rows.append(dict(kind=kind, theta=theta, ve_over_vd=ve_vd,
                                       P_med=np.nanmedian(arr[:, 0]),
                                       P_q25=np.nanpercentile(arr[:, 0], 25),
                                       P_q75=np.nanpercentile(arr[:, 0], 75),
                                       n_hiat_med=np.median(arr[:, 1])))
    pd.concat(all_runs).to_csv(f"{SYN}/ensemble_runs.csv", index=False)
    pd.concat(all_hiats).to_csv(f"{SYN}/ensemble_hiatuses.csv", index=False)
    pd.DataFrame(sweep_rows).to_csv(f"{SYN}/sensitivity_sweep.csv", index=False)
    print("sweep rows:", len(sweep_rows))


if __name__ == "__main__":
    main()
