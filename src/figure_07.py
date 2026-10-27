"""Figure 7: Case II hiatus CCDFs by forcing class, compared with Case I.
(a) Synthetic CCDFs (pooled per class, full resolution).
(b) Same truncated at >= 0.5 Myr (comparable to Macrostrat resolution) with
    power-law fits.
(c) Exponent comparison real vs synthetic (bar chart with bootstrap CIs).
(d) Scaling range (xmin to max) real vs synthetic.
Data: data/synthetic/ensemble_hiatuses.csv; data/processed/hiatus_powerlaw_fits.csv.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from figures_common import setup, save, FCOLORS, FLABELS, SYN, PROC, SETTING_SHORT
import sys
sys.path.insert(0, str(ROOT / "src"))
from analysis import plfit

setup()
hh = pd.read_csv(f"{SYN}/ensemble_hiatuses.csv")
fits_real = pd.read_csv(f"{PROC}/hiatus_powerlaw_fits.csv")

def title(ax, s):
    ax.set_title(s, loc="left", fontsize=8.5, fontweight="bold", pad=3)

fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.0))
ax = axes[0, 0]
for k in ["F1", "F2", "F3"]:
    x = np.sort(hh[hh["kind"] == k]["hiatus_myr"].values)[::-1]
    ax.loglog(x, np.arange(1, len(x) + 1) / len(x), ".", ms=1.4, color=FCOLORS[k], label=FLABELS[k])
ax.set_xlabel("Hiatus duration (Myr)"); ax.set_ylabel("P(H > $h$)")
ax.legend(fontsize=6.2, markerscale=3, loc="lower left")
title(ax, "(a) Synthetic CCDFs, full resolution")

ax = axes[0, 1]
alphas_syn = {}
for k in ["F1", "F2", "F3"]:
    x = hh[hh["kind"] == k]["hiatus_myr"].values
    x = x[x >= 0.5]
    if len(x) > 30:
        f = plfit(x)
        alphas_syn[k] = f
        xs = np.sort(x)[::-1]
        ax.loglog(xs, np.arange(1, len(xs) + 1) / len(xs), ".", ms=1.6, color=FCOLORS[k],
                  label=f"{k}: $\\alpha$={f['alpha']:.2f}")
        xx = np.logspace(np.log10(f["xmin"]), np.log10(xs.max()), 30)
        ax.loglog(xx, (f["n_tail"] / len(xs)) * (xx / f["xmin"]) ** (1 - f["alpha"]),
                  color=FCOLORS[k], lw=1.1)
ax.set_xlabel("Hiatus duration (Myr, $\\geq$0.5)"); ax.set_ylabel("P(H > $h$)")
ax.set_ylim(2e-3, 3)
ax.legend(fontsize=6.2, markerscale=3, loc="lower left")
title(ax, "(b) Truncated to Macrostrat resolution")

ax = axes[1, 0]
heavy = fits_real[fits_real["llr_powerlaw_vs_exp"] > 10]
labels = [SETTING_SHORT[s] for s in heavy["setting"]] + [f"SYN-{k}" for k in alphas_syn]
vals = list(heavy["alpha"]) + [alphas_syn[k]["alpha"] for k in alphas_syn]
errs = [(v - l, h - v) for v, l, h in zip(heavy["alpha"], heavy["alpha_lo"], heavy["alpha_hi"])] + \
       [(0, 0)] * len(alphas_syn)
cols = ["#21618C"] * len(heavy) + ["#B03A2E"] * len(alphas_syn)
ax.bar(range(len(vals)), vals, yerr=np.array(errs).T, color=cols, capsize=2)
ax.set_xticks(range(len(vals)))
ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=6.2)
ax.set_ylabel("Power-law exponent $\\alpha$"); ax.set_ylim(0, 6.2)
title(ax, "(c) Exponents: real vs synthetic")

ax = axes[1, 1]
names = [SETTING_SHORT[s] for s in fits_real["setting"]] + [f"SYN-{k}" for k in alphas_syn]
xmins = list(fits_real["xmin"]) + [alphas_syn[k]["xmin"] for k in alphas_syn]
xmaxs = list(fits_real["max"]) + [hh[hh["kind"] == k]["hiatus_myr"].max() for k in alphas_syn]
cols2 = ["#21618C"] * len(fits_real) + ["#B03A2E"] * len(alphas_syn)
for i, (a, b, c) in enumerate(zip(xmins, xmaxs, cols2)):
    ax.plot([a, b], [i, i], "-", color=c, lw=3, solid_capstyle="butt")
ax.set_xscale("log"); ax.set_yticks(range(len(names)))
ax.set_yticklabels(names, fontsize=6.4)
ax.set_xlabel("Scaling range (Myr): $x_{min}$ \u2192 max observed")
ax.set_ylim(-0.6, len(names) - 0.4)
title(ax, "(d) Fitted scaling ranges")
fig.tight_layout()
save(fig, "figure_07_caseII_hiatus_compare")
