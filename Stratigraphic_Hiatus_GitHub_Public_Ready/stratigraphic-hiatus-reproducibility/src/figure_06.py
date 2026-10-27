
"""Figure 6: Case II model definition and example synthetic columns.

Only plot layout, fonts and legend locations are changed.
Scientific models, parameters and random seeds are unchanged.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import matplotlib.pyplot as plt
import sys

from figures_common import (
    setup, save, FCOLORS, FLABELS
)

sys.path.insert(0, str(ROOT / "src"))

from simulation import make_driver, run_column, MASTER_SEED

setup()

# =====================================================
# 1. Unified figure layout
# =====================================================

TITLE_SIZE = 11.5
LABEL_SIZE = 8.8
TICK_SIZE = 7.8
LEGEND_SIZE = 7.0

fig, axes = plt.subplots(
    2, 2, figsize=(10.8, 8.0)
)

fig.subplots_adjust(
    left=0.085,
    right=0.98,
    bottom=0.105,
    top=0.93,
    wspace=0.26,
    hspace=0.34
)

def style_panel(ax, title):
    ax.set_title(
        title,
        loc="left",
        pad=10,
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )
    ax.tick_params(
        axis="both", which="major",
        labelsize=TICK_SIZE
    )
    ax.tick_params(
        axis="both", which="minor",
        labelsize=TICK_SIZE
    )
    ax.xaxis.label.set_size(LABEL_SIZE)
    ax.yaxis.label.set_size(LABEL_SIZE)


# =====================================================
# 2. Original simulation settings
# =====================================================

dt_kyr, T_myr = 0.5, 5.0
n = int(T_myr * 1000 / dt_kyr)
t = np.arange(n) * dt_kyr / 1000.0


# =====================================================
# (a) Forcing classes
# =====================================================

ax = axes[0, 0]
driver_max = -np.inf

for k in ["F1", "F2", "F3"]:
    rng = np.random.default_rng(MASTER_SEED + 5)
    u = make_driver(k, n, dt_kyr, rng)

    # Only used to reserve blank space for the legend
    driver_max = max(
        driver_max, np.max(u[:3000])
    )

    ax.plot(
        t[:3000], u[:3000],
        lw=0.5,
        color=FCOLORS[k],
        label=FLABELS[k]
    )

ax.axhline(
    0.5, color="green", ls="--", lw=0.8
)
ax.axhline(
    -0.5, color="red", ls="--", lw=0.8
)

ax.text(
    0.02, 0.60, "$\\theta_d$",
    fontsize=7, color="green",
    ha="left", va="bottom"
)

ax.text(
    0.02, -0.60, "$-\\theta_e$",
    fontsize=7, color="red",
    ha="left", va="top"
)

ax.set_xlabel("Time (Myr)")
ax.set_ylabel("Driver $u(t)$ (standardised)")

# Display range only; does not modify any u values
ax.set_ylim(top=driver_max + 1.6)

ax.legend(
    fontsize=LEGEND_SIZE,
    ncol=1,
    loc="upper right",
    bbox_to_anchor=(0.985, 0.985),
    frameon=True,
    framealpha=0.96,
    facecolor="white",
    edgecolor="#B0B0B0",
    fancybox=False,
    borderpad=0.35,
    handlelength=2.0,
    labelspacing=0.32
)

style_panel(ax, "(a) Forcing classes")


# =====================================================
# (b) Switching rule
# =====================================================

ax = axes[0, 1]

u = np.linspace(-3, 3, 400)

state = np.where(
    u > 0.5, 1,
    np.where(u < -0.5, -1, 0)
)

ax.fill_between(
    u, 0, 1,
    where=state == 1,
    color="#A9DFBF"
)
ax.fill_between(
    u, 0, 1,
    where=state == 0,
    color="#F9E79F"
)
ax.fill_between(
    u, 0, 1,
    where=state == -1,
    color="#F5B7B1"
)

ax.text(
    -2.0, 0.5, "Erosion",
    ha="center", va="center",
    fontsize=7.5, color="#922B21"
)
ax.text(
    0.0, 0.5, "Stasis",
    ha="center", va="center",
    fontsize=7.5, color="#7D6608"
)
ax.text(
    1.75, 0.5, "Deposition",
    ha="center", va="center",
    fontsize=7.5, color="#1E8449"
)

ax.axvline(
    0.5, color="green", ls="--", lw=0.8
)
ax.axvline(
    -0.5, color="red", ls="--", lw=0.8
)


ax.annotate(
    r"$-\theta_e$",
    xy=(-0.5, -0.12),
    xytext=(-8, 0),
    textcoords="offset points",
    ha="right",
    va="center",
    fontsize=8,
    color="red"
)

ax.annotate(
    r"$\theta_d$",
    xy=(0.5, -0.12),
    xytext=(8, 0),
    textcoords="offset points",
    ha="left",
    va="center",
    fontsize=8,
    color="green"
)


ax.set_xlabel("Driver $u$")
ax.set_xlim(-3, 3)
ax.set_ylim(-0.25, 1.0)
ax.set_yticks([])

style_panel(ax, "(b) Switching rule")


# =====================================================
# (c) Age-depth columns
# (d) Surviving depositional time
# =====================================================

ax = axes[1, 0]
ax2 = axes[1, 1]

runs = {}

for i, k in enumerate(["F1", "F2", "F3"]):

    # Original simulation: no manually assigned results
    r = run_column(k, MASTER_SEED + 42)

    runs[k] = r

    ages, depths = [0.0], [0.0]
    cum = 0.0

    for t0, t1, th in r["layers"]:
        ages += [t0, t1]
        depths += [cum, cum + th]
        cum += th

    ax.plot(
        ages[1:],
        np.maximum(depths[1:], 5e-2),
        lw=1.0,
        color=FCOLORS[k],
        label=f"{k}: P={r['P']:.2f}"
    )

    # Original surviving depositional intervals
    bars = [
        (t0, t1 - t0)
        for t0, t1, th in r["layers"]
    ]

    ax2.broken_barh(
        bars,
        (2 - i - 0.38, 0.76),
        facecolors=FCOLORS[k],
        alpha=0.85
    )

# Panel (c)
ax.set_yscale("log")
ax.set_xlabel("Depositional time (Myr)")
ax.set_ylabel("Preserved thickness (m, log)")

ax.legend(
    fontsize=LEGEND_SIZE,
    loc="upper left",
    bbox_to_anchor=(0.02, 0.975),
    frameon=True,
    framealpha=0.96,
    facecolor="white",
    edgecolor="#B0B0B0",
    fancybox=False,
    borderpad=0.35,
    labelspacing=0.35,
    handlelength=2.0
)

ax.margins(y=0.15)

style_panel(
    ax, "(c) Preserved age-depth columns"
)

# Panel (d)
ax2.set_xlim(0, T_myr)
ax2.set_ylim(-0.6, 2.6)

ax2.set_yticks([0, 1, 2])
ax2.set_yticklabels(["F3", "F2", "F1"])

ax2.set_xlabel("Depositional time (Myr)")

style_panel(
    ax2, "(d) Surviving depositional time"
)

# =====================================================
# Save
# =====================================================

save(fig, "figure_06_caseII_model")

print("Figure 6 generated successfully.")
