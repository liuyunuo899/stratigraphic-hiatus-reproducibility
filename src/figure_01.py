"""Figure 1: Conceptual framework of the synthesis.
(a) Causal chain from forcing to preservation. (b) Forward vs inverse problem.
(c) The three literature blocks this review connects. Purely conceptual, drawn
with matplotlib primitives; no data.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from figures_common import setup, save

setup()
fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.7))

def box(ax, xy, w, h, text, fc="#EAF2F8", ec="#21618C", fs=6.4):
    ax.add_patch(FancyBboxPatch(xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                fc=fc, ec=ec, lw=0.9))
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fs)

def arrow(ax, p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=9,
                                 lw=1.0, color="#555555"))

def heading(ax, text):
    ax.set_title(text, loc="left", fontsize=8.0, fontweight="bold", pad=4)

# (a) causal chain -----------------------------------------------------------
ax = axes[0]; ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
labels = ["Environmental forcing\n(sea level, supply, tectonics)",
          "Depositional-state switching\n(deposition / stasis / erosion)",
          "Hiatus duration\nstatistics $N(>\\tau)$",
          "Temporal\ncompleteness $C(\\tau)$",
          "Mass preservation\nefficiency $P$"]
h, w, x0 = 0.13, 0.86, 0.07
ys = [0.82, 0.625, 0.43, 0.235, 0.04]
for lab, y in zip(labels, ys):
    box(ax, (x0, y), w, h, lab, fs=6.2)
for y1, y2 in zip(ys[:-1], ys[1:]):
    arrow(ax, (0.5, y1), (0.5, y2 + h))
heading(ax, "(a) Mechanism chain")

# (b) forward vs inverse -----------------------------------------------------
ax = axes[1]; ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
bw, bh = 0.42, 0.24
box(ax, (0.03, 0.70), bw, bh, "Forward model\n$h(t)$, $d(t)$, $e(t)$\n$\\rightarrow$ preserved record",
    fc="#FEF9E7", ec="#B7950B", fs=6.0)
box(ax, (0.03, 0.08), bw, bh, "Final age\u2013depth data\n$\\{(t_i, z_i, \\sigma_i)\\}$",
    fc="#FEF9E7", ec="#B7950B", fs=6.0)
box(ax, (0.55, 0.70), bw, bh, "Variational inversion\n$J = J_{obs} + \\lambda J_{prior}$\n(minimise)",
    fc="#FDEDEC", ec="#922B21", fs=6.0)
box(ax, (0.55, 0.08), bw, bh, "Admissible histories\nensemble (non-unique)\n$\\rightarrow$ spread of $P$",
    fc="#FDEDEC", ec="#922B21", fs=6.0)
arrow(ax, (0.24, 0.70), (0.24, 0.34)); arrow(ax, (0.45, 0.82), (0.55, 0.82))
arrow(ax, (0.76, 0.70), (0.76, 0.34)); arrow(ax, (0.45, 0.20), (0.55, 0.20))
heading(ax, "(b) Forward\u2013inverse structure")

# (c) three literature blocks -------------------------------------------------
ax = axes[2]; ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
box(ax, (0.02, 0.68), 0.58, 0.26, "Completeness &\nthe Sadler effect\n(Sadler 1981; Kemp 2012;\nHagen 2024)",
    fc="#E8F8F5", ec="#148F77", fs=6.0)
box(ax, (0.02, 0.37), 0.58, 0.26, "Hiatus scaling &\nstratigraphic filter\n(Plotnick 1986; Schumer\net al. 2009, 2011)",
    fc="#F4ECF7", ec="#7D3C98", fs=6.0)
box(ax, (0.02, 0.06), 0.58, 0.26, "Sediment preservation\n& recycling\n(Veizer & Jansen 1979;\nPeters & Husson 2017)",
    fc="#FDF2E9", ec="#CA6F1E", fs=6.0)
box(ax, (0.68, 0.37), 0.30, 0.26, "This review:\none coupled\nframework",
    fc="#EAEDED", ec="#1B2631", fs=6.4)
arrow(ax, (0.60, 0.81), (0.74, 0.63)); arrow(ax, (0.60, 0.50), (0.68, 0.50))
arrow(ax, (0.60, 0.19), (0.74, 0.37))
heading(ax, "(c) Connected literatures")

fig.tight_layout()
save(fig, "figure_01_framework")
