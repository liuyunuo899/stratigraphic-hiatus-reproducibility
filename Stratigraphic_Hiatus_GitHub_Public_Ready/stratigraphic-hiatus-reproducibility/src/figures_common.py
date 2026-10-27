"""Shared style and IO helpers for all figures."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

FIGDIR = str(ROOT / "figures")
PROC = str(ROOT / "data/processed")
SYN = str(ROOT / "data/synthetic")

SETTING_ORDER = ["Cratonic platform", "Passive margin & coastal plain", "Foreland (Rocky Mtn.)",
                 "Appalachian orogen", "Cordilleran & Alaska orogen", "Shield & Arctic"]
SETTING_SHORT = {"Cratonic platform": "Cratonic platform",
                 "Passive margin & coastal plain": "Passive margin",
                 "Foreland (Rocky Mtn.)": "Foreland (Rocky Mtn.)",
                 "Appalachian orogen": "Appalachian orogen",
                 "Cordilleran & Alaska orogen": "Cordilleran/Alaska",
                 "Shield & Arctic": "Shield & Arctic"}
PALETTE = dict(zip(SETTING_ORDER,
                   ["#0072B2", "#009E73", "#E69F00", "#D55E00", "#CC79A7", "#666666"]))
FCOLORS = {"F1": "#56B4E9", "F2": "#E69F00", "F3": "#D55E00"}
FLABELS = {"F1": "F1 white-noise", "F2": "F2 multi-periodic", "F3": "F3 long-memory"}


def setup():
    plt.rcParams.update({
        "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
        "figure.dpi": 150, "savefig.dpi": 400, "lines.linewidth": 1.2,
        "axes.linewidth": 0.8, "axes.grid": True, "grid.alpha": 0.25,
        "grid.linewidth": 0.4, "font.family": "DejaVu Sans",
    })


def panel_label(ax, s):
    ax.text(0.02, 0.97, s, transform=ax.transAxes, fontweight="bold",
            fontsize=9, va="top", ha="left")


def save(fig, name):
    fig.savefig(f"{FIGDIR}/{name}.pdf", bbox_inches="tight")
    fig.savefig(f"{FIGDIR}/{name}.png", bbox_inches="tight")
    plt.close(fig)
    print("saved", name)
