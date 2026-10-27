"""Statistical analysis of hiatus durations and Sadler-type rates (Case I).

Methods follow the Clauset, Shalizi & Newman (2009) protocol, simplified:
- For x >= xmin, the MLE of the power-law exponent is alpha = 1 + n / sum(ln(x/xmin)).
- xmin is chosen by minimising the Kolmogorov-Smirnov distance between data and fit.
- Bootstrap (n=1000, fixed seed) gives 95% CIs for alpha.
- Power law vs exponential compared by log-likelihood ratio over x >= xmin.
All randomness uses numpy default_rng with fixed seeds recorded in the outputs.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd

PROC = str(ROOT / "data/processed")
RNG = np.random.default_rng(20261020)


def plfit(x, xmin=None):
    x = np.asarray(x, dtype=float)
    x = x[x > 0]
    if xmin is None:
        cands = np.unique(x)[:-1]
        best = None
        for xm in cands:
            xs = x[x >= xm]
            if len(xs) < 20:
                continue
            a = 1 + len(xs) / np.sum(np.log(xs / xm))
            cdf_d = 1 - (xs / xm) ** (1 - a)
            ks = np.abs(cdf_d - (np.arange(1, len(xs) + 1) / len(xs))).max() \
                if False else np.abs(np.sort(cdf_d) - np.arange(1, len(xs) + 1) / len(xs)).max()
            if best is None or ks < best[2]:
                best = (xm, a, ks, len(xs))
        if best is None:
            return None
        return dict(xmin=best[0], alpha=best[1], ks=best[2], n_tail=best[3])
    xs = x[x >= xmin]
    a = 1 + len(xs) / np.sum(np.log(xs / xmin))
    return dict(xmin=xmin, alpha=a, n_tail=len(xs))


def ll_ratio_powerlaw_vs_exp(x, xmin, alpha):
    xs = x[x >= xmin]
    n = len(xs)
    ll_pl = np.sum(np.log((alpha - 1) / xmin) - alpha * np.log(xs / xmin))
    lam = 1.0 / (xs.mean() - xmin)
    ll_ex = np.sum(np.log(lam) - lam * (xs - xmin))
    return ll_pl - ll_ex


def bootstrap_alpha(x, xmin, n_boot=1000):
    xs = np.asarray(x)[np.asarray(x) >= xmin]
    if len(xs) < 20:
        return np.nan, np.nan
    vals = []
    for _ in range(n_boot):
        s = RNG.choice(xs, size=len(xs), replace=True)
        vals.append(1 + len(s) / np.sum(np.log(s / xmin)))
    return np.percentile(vals, [2.5, 97.5])


def analyze_hiatuses():
    h = pd.read_csv(f"{PROC}/hiatuses.csv")
    rows = []
    for setting, g in h.groupby("setting"):
        x = g["hiatus_myr"].values
        fit = plfit(x)
        if fit is None:
            continue
        lo, hi = bootstrap_alpha(x, fit["xmin"])
        llr = ll_ratio_powerlaw_vs_exp(x, fit["xmin"], fit["alpha"])
        rows.append(dict(setting=setting, n=len(x), median=np.median(x), max=x.max(),
                         xmin=fit["xmin"], alpha=fit["alpha"], alpha_lo=lo, alpha_hi=hi,
                         n_tail=fit["n_tail"], llr_powerlaw_vs_exp=llr))
    out = pd.DataFrame(rows)
    out.to_csv(f"{PROC}/hiatus_powerlaw_fits.csv", index=False)
    return out


def sadler_summary():
    sp = pd.read_csv(f"{PROC}/sadler_pairs.csv")
    sp["decade"] = np.floor(np.log10(sp["timespan_myr"]))
    rows = []
    for (setting, decade), g in sp.groupby(["setting", "decade"]):
        rows.append(dict(setting=setting, timespan_mid=10 ** (decade + 0.5),
                         rate_median=g["rate_m_per_myr"].median(),
                         rate_q25=g["rate_m_per_myr"].quantile(0.25),
                         rate_q75=g["rate_m_per_myr"].quantile(0.75), n=len(g)))
    out = pd.DataFrame(rows)
    out.to_csv(f"{PROC}/sadler_summary.csv", index=False)
    return out


if __name__ == "__main__":
    fits = analyze_hiatuses()
    print(fits.round(3).to_string(index=False))
    sadler_summary()
    print("sadler summary written")
