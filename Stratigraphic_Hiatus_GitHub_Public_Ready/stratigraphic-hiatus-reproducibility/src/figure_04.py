
"""Figure 4: Case I hiatus-duration CCDFs by tectonic setting.

Six panels showing empirical CCDFs and power-law fits.
Only figure layout and typography are modified.
Original data, parameters, and calculations are unchanged.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figures_common import (
    setup, save, SETTING_ORDER,
    SETTING_SHORT, PALETTE, PROC
)

setup()

# =====================================================
# 1. Read original data
# =====================================================

h = pd.read_csv(f"{PROC}/hiatuses.csv")

fits = pd.read_csv(
    f"{PROC}/hiatus_powerlaw_fits.csv"
).set_index("setting")

# =====================================================
# 2. Unified figure style
# =====================================================

TITLE_SIZE = 11.5
LABEL_SIZE = 8.8
TICK_SIZE = 7.8
LEGEND_SIZE = 7.0

fig, axes = plt.subplots(
    2, 3,
    figsize=(10.8, 7.2)
)

fig.subplots_adjust(
    left=0.075,
    right=0.984,
    bottom=0.105,
    top=0.930,
    wspace=0.35,
    hspace=0.55
)

# =====================================================
# 3. Plot each tectonic setting
# =====================================================

for i, (ax, st) in enumerate(
    zip(axes.flat, SETTING_ORDER)
):

    # Original empirical CCDF calculation
    x = np.sort(
        h[h["setting"] == st]["hiatus_myr"].values
    )[::-1]

    ccdf = np.arange(1, len(x) + 1) / len(x)

    ax.loglog(
        x,
        ccdf,
        ".",
        ms=2.5,
        color=PALETTE[st],
        alpha=0.55
    )

    # Original power-law fitting parameters
    f = fits.loc[st]

    xm = f["xmin"]
    a = f["alpha"]

    xx = np.logspace(
        np.log10(xm),
        np.log10(x.max()),
        50
    )

    n_tail = f["n_tail"]
    n_all = len(x)

    ccdf_xm = n_tail / n_all
    llr = f["llr_powerlaw_vs_exp"]

    # Avoid displaying small negative LLR as -0
    llr_label = (
        f"{llr:.2f}"
        if abs(llr) < 1
        else f"{llr:.0f}"
    )

    ax.loglog(
        xx,
        ccdf_xm * (xx / xm) ** (1 - a),
        "-",
        color="black",
        lw=1.3,
        label=(
            f"$\\alpha$={a:.2f} "
            f"[{f['alpha_lo']:.2f}, "
            f"{f['alpha_hi']:.2f}]\n"
            f"LLR={llr_label}, n={n_all}"
        )
    )

    # xmin reference line
    ax.axvline(
        xm,
        color="grey",
        ls=":",
        lw=0.8
    )

    ax.text(
        xm * 1.12,
        0.965,
        "$x_{min}$",
        fontsize=7.0,
        color="grey",
        va="top",
        ha="left",
        transform=ax.get_xaxis_transform()
    )

    # =================================================
    # Panel title
    # =================================================

    ax.set_title(
        f"({'abcdef'[i]}) {SETTING_SHORT[st]}",
        fontsize=TITLE_SIZE,
        fontweight="bold",
        loc="left",
        pad=10
    )

    # =================================================
    # Axis labels and tick labels
    # =================================================

    ax.set_xlabel(
        "Hiatus duration (Myr)",
        fontsize=LABEL_SIZE,
        labelpad=5
    )

    ax.set_ylabel(
        "P(H > $h$)",
        fontsize=LABEL_SIZE,
        labelpad=4
    )

    ax.tick_params(
        axis="both",
        which="major",
        labelsize=TICK_SIZE,
        pad=3
    )

    ax.tick_params(
        axis="both",
        which="minor",
        labelsize=TICK_SIZE,
        pad=3
    )

    # =================================================
    # Statistical legend
    # =================================================

    ax.legend(
        fontsize=LEGEND_SIZE,
        loc="lower left",
        bbox_to_anchor=(0.025, 0.025),
        borderaxespad=0.0,
        frameon=True,
        facecolor="white",
        edgecolor="#B6B6B6",
        framealpha=0.95,
        fancybox=False,
        borderpad=0.35,
        handlelength=1.5,
        handletextpad=0.5,
        labelspacing=0.3
    )

# =====================================================
# 4. Save figure
# =====================================================

save(fig, "figure_04_caseI_hiatus_ccdf")

print("Figure 4 generated successfully.")
