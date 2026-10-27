
"""Figure 9: Identifiability of depositional history.

Only layout, typography, and legend positions are changed.
All data, calculations and random seeds remain unchanged.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from figures_common import setup, save, SYN

sys.path.insert(0, str(ROOT / "src"))
from inversion import build_truth, SEED

setup()

# Read actual calculated data
obs = pd.read_csv(f"{SYN}/inversion_observations.csv")
curves = pd.read_csv(f"{SYN}/inversion_curves.csv")
ens = pd.read_csv(f"{SYN}/inversion_ensemble.csv")

ages, depths, truth = build_truth()

# Unified layout
TITLE_SIZE = 11.5
LABEL_SIZE = 8.8
TICK_SIZE = 7.8
LEGEND_SIZE = 7.0

fig, axes = plt.subplots(2, 2, figsize=(10.8, 8.2))

fig.subplots_adjust(
    left=0.085,
    right=0.985,
    bottom=0.105,
    top=0.925,
    wspace=0.28,
    hspace=0.37
)

def format_panel(ax, title):
    ax.set_title(
        title,
        loc="left",
        fontsize=TITLE_SIZE,
        fontweight="bold",
        pad=10
    )
    ax.xaxis.label.set_size(LABEL_SIZE)
    ax.yaxis.label.set_size(LABEL_SIZE)
    ax.tick_params(
        axis="both", which="major",
        labelsize=TICK_SIZE
    )
    ax.tick_params(
        axis="both", which="minor",
        labelsize=TICK_SIZE
    )

legend_style = dict(
    fontsize=LEGEND_SIZE,
    frameon=True,
    facecolor="white",
    edgecolor="#B0B0B0",
    framealpha=0.96,
    fancybox=False,
    borderpad=0.35,
    labelspacing=0.32,
    handlelength=2.0,
    handletextpad=0.5
)

# =====================================================
# (a) Record, data, smooth inversions
# =====================================================

ax = axes[0, 0]

ax.plot(
    ages, depths, "k-", lw=1.6,
    label="True preserved record"
)

ax.errorbar(
    obs["t_obs"],
    obs["z_obs"],
    xerr=2 * obs["sigma_t"],
    fmt="o",
    ms=3,
    color="#21618C",
    label="Dated horizons (2$\\sigma_t$)"
)

for lam, col in [
    (0.1, "#F5B7B1"),
    (1, "#F0B27A"),
    (10, "#AF7AC5"),
    (100, "#5499C7")
]:
    g = curves[curves["lam"] == lam]

    ax.plot(
        g["t"],
        np.cumsum(g["rate"]) *
        (g["t"].iloc[1] - g["t"].iloc[0]),
        lw=0.9,
        color=col,
        label=f"$\\lambda$={lam:g}"
    )

ax.set_xlabel("Time (Myr)")
ax.set_ylabel("Preserved thickness (m)")

ax.legend(
    loc="upper left",
    bbox_to_anchor=(0.025, 0.81),
    ncol=1,
    borderaxespad=0,
    **legend_style
)

format_panel(
    ax, "(a) Record, data, smooth inversions"
)

# =====================================================
# (b) Admissible gross mass
# =====================================================

ax = axes[0, 1]

ax.hist(
    ens["M_gross"],
    bins=60,
    color="#5D6D7E",
    alpha=0.85
)

ax.axvline(
    truth["M_gross"],
    color="#C0392B",
    lw=1.5,
    label="True $M_{gross}$"
)

ax.axvline(
    ens["M_gross"].median(),
    color="#1B4F72",
    ls="--",
    lw=1.2,
    label="Admissible median"
)

ax.set_xlabel("Gross deposited mass $M_{gross}$ (m)")
ax.set_ylabel("Count")
ax.margins(y=0.18)

ax.legend(
    loc="upper left",
    bbox_to_anchor=(0.42, 0.84),
    ncol=1,
    borderaxespad=0,
    **legend_style
)

format_panel(
    ax, "(b) Admissible gross mass"
)

# =====================================================
# (c) Admissible preservation efficiency
# =====================================================

ax = axes[1, 0]

ax.hist(
    ens["P"],
    bins=60,
    color="#7D6608",
    alpha=0.85
)

ax.axvline(
    truth["P"],
    color="#C0392B",
    lw=1.5,
    label="True P"
)

ax.axvline(
    ens["P"].median(),
    color="#1B4F72",
    ls="--",
    lw=1.2,
    label="Admissible median"
)

ax.set_xlabel("Preservation efficiency P")
ax.set_ylabel("Count")
ax.margins(y=0.18)

ax.legend(
    loc="upper left",
    bbox_to_anchor=(0.27, 0.93),
    ncol=1,
    borderaxespad=0,
    **legend_style
)

format_panel(
    ax, "(c) Admissible preservation efficiency"
)

# =====================================================
# (d) Misfit vs smoothing
# =====================================================

ax = axes[1, 1]

ms = []

for lam in sorted(curves["lam"].unique()):
    g = curves[curves["lam"] == lam]

    zg = (
        np.cumsum(g["rate"].values)
        * (g["t"].iloc[1] - g["t"].iloc[0])
    )

    zpred = np.interp(
        obs["t_obs"],
        g["t"],
        zg
    )

    chi2 = np.sum(
        ((zpred - obs["z_obs"]) / obs["sigma_z"]) ** 2
    ) / len(obs)

    ms.append(chi2)

ax.loglog(
    sorted(curves["lam"].unique()),
    ms,
    "o-",
    color="#117A65"
)

ax.axhline(
    1.0,
    color="grey",
    ls=":",
    lw=0.8
)

ax.set_xlabel("Smoothing weight $\\lambda$")
ax.set_ylabel("Reduced $\\chi^2$")

ax.set_ylim(
    min(ms) * 0.5,
    max(max(ms) * 2, 2)
)

format_panel(
    ax, "(d) Misfit vs smoothing"
)

# =====================================================
# Save
# =====================================================

# Positions have been adjusted manually.
# Do not apply tight_layout().

save(fig, "figure_09_identifiability")

print("Figure 9 generated successfully.")
