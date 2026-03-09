"""
plotter.py
==========
Generates a dark-themed, multi-panel matplotlib summary report
saved as 'simulation_report.png' in the simulation folder.
"""

import os
import math
import matplotlib
matplotlib.use("Agg")          # headless backend – no tkinter needed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MaxNLocator


# ── Palette ────────────────────────────────────────────────────
BG_DARK    = "#0d1117"
BG_PANEL   = "#161b22"
GRID_COL   = "#21262d"
BORDER_COL = "#30363d"

C_MOISTURE = "#58a6ff"   # blue
C_EC       = "#f0c040"   # amber
C_PH       = "#c084fc"   # violet
C_TEMP     = "#fb923c"   # orange
C_IRR      = "#22d3ee"   # cyan
C_MICRO    = "#f0c040"   # amber
C_MACRO    = "#4ade80"   # green
C_WARN     = "#f85149"   # red

LABEL_KW   = dict(color="white", fontsize=9, fontweight="bold")
TITLE_KW   = dict(color="white", fontsize=11, fontweight="bold", pad=8)
LEGEND_KW  = dict(fontsize=8, facecolor=BG_PANEL, edgecolor=BORDER_COL,
                  labelcolor="white")


def _style_ax(ax: plt.Axes) -> None:
    ax.set_facecolor(BG_PANEL)
    ax.grid(True, color=GRID_COL, linewidth=0.6, alpha=0.8)
    ax.spines[:].set_color(BORDER_COL)
    ax.tick_params(colors="white", labelsize=8)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color("white")


def _threshold_line(ax, y, color, label):
    ax.axhline(y, color=color, linestyle="--", linewidth=0.9,
               alpha=0.75, label=label)


# ──────────────────────────────────────────────────────────────
def plot_simulation(history: list[dict], output_path: str = "simulation_report.png") -> str:
    """
    Build a 3×2 grid dashboard and save to *output_path*.
    Returns the resolved file path.
    """
    steps    = [h["step"]      for h in history]
    moisture = [h["moisture"]  for h in history]
    ec       = [h["ec"]        for h in history]
    ph       = [h["ph"]        for h in history]
    temp     = [h["temp"]      for h in history]
    irr      = [int(h["irr"])  for h in history]
    micro    = [int(h["micro"]) for h in history]
    macro    = [int(h["macro"]) for h in history]

    fig = plt.figure(figsize=(15, 11), facecolor=BG_DARK)
    gs  = GridSpec(3, 2, figure=fig, hspace=0.50, wspace=0.35,
                   top=0.93, bottom=0.06, left=0.07, right=0.97)

    # ── 1. Soil Moisture ───────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(steps, moisture, color=C_MOISTURE, linewidth=2,
             label="Moisture %", zorder=3)
    ax1.fill_between(steps, moisture, alpha=0.15, color=C_MOISTURE)
    _threshold_line(ax1, 35, C_WARN,  "Low  (35%)")
    _threshold_line(ax1, 75, "#4ade80", "High (75%)")
    ax1.fill_between(steps, moisture, 35,
                     where=[m < 35 for m in moisture],
                     alpha=0.25, color=C_WARN, label="Dry zone")
    ax1.set_title("Soil Moisture (%)", **TITLE_KW)
    ax1.set_ylabel("%", **LABEL_KW)
    ax1.set_ylim(0, 110)
    ax1.legend(**LEGEND_KW)
    _style_ax(ax1)

    # ── 2. EC Level ────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(steps, ec, color=C_EC, linewidth=2,
             label="EC (mS/cm)", zorder=3)
    ax2.fill_between(steps, ec, alpha=0.15, color=C_EC)
    _threshold_line(ax2, 1.0, C_WARN,    "Low  (1.0)")
    _threshold_line(ax2, 3.0, "#4ade80", "High (3.0)")
    ax2.set_title("Electrical Conductivity (mS/cm)", **TITLE_KW)
    ax2.set_ylabel("mS/cm", **LABEL_KW)
    ax2.legend(**LEGEND_KW)
    _style_ax(ax2)

    # ── 3. pH ──────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(steps, ph, color=C_PH, linewidth=2,
             label="pH", zorder=3)
    ax3.fill_between(steps, ph, alpha=0.15, color=C_PH)
    _threshold_line(ax3, 5.5, C_WARN,    "Low  (5.5)")
    _threshold_line(ax3, 7.0, "#4ade80", "High (7.0)")
    ax3.set_title("pH Level", **TITLE_KW)
    ax3.set_ylabel("pH", **LABEL_KW)
    ax3.set_ylim(4.5, 9.0)
    ax3.legend(**LEGEND_KW)
    _style_ax(ax3)

    # ── 4. Temperature ─────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(steps, temp, color=C_TEMP, linewidth=2,
             label="Temp (°C)", zorder=3)
    ax4.fill_between(steps, temp, alpha=0.15, color=C_TEMP)
    ax4.set_title("Temperature (°C) – Day/Night Cycle", **TITLE_KW)
    ax4.set_ylabel("°C", **LABEL_KW)
    ax4.legend(**LEGEND_KW)
    _style_ax(ax4)

    # ── 5. Pump Activity (stacked bands) ───────────────────────
    ax5 = fig.add_subplot(gs[2, :])
    gap = 0.08   # gap between bands

    # Irrigation band: y 2.0 – 3.0
    irr_hi  = [2.0 + v * (1.0 - gap) for v in irr]
    micro_hi= [1.0 + v * (1.0 - gap) for v in micro]
    macro_hi= [0.0 + v * (1.0 - gap) for v in macro]

    ax5.fill_between(steps, 2.0, irr_hi,   alpha=0.85, color=C_IRR,   label="💧 Irrigation Pump")
    ax5.fill_between(steps, 1.0, micro_hi, alpha=0.85, color=C_MICRO,  label="🧪 Micro-Nutrient Pump")
    ax5.fill_between(steps, 0.0, macro_hi, alpha=0.85, color=C_MACRO,  label="🌿 Macro-Nutrient Pump")

    ax5.set_yticks([0.45, 1.45, 2.45])
    ax5.set_yticklabels(["Macro", "Micro", "Irrigation"], color="white", fontsize=9)
    ax5.set_ylim(0, 3)
    ax5.set_title("Pump Activity Timeline (ON = filled)", **TITLE_KW)
    ax5.set_xlabel("Simulation Step", **LABEL_KW)
    ax5.legend(**LEGEND_KW, loc="upper right", ncol=3)
    _style_ax(ax5)

    # ── Main title ─────────────────────────────────────────────
    n = len(history)
    fig.suptitle(
        f"Smart Plant Micro-Macro Nutrient Doser – Simulation Report  "
        f"({n} steps)",
        fontsize=14, fontweight="bold", color="white", y=0.975,
    )

    # ── Save ───────────────────────────────────────────────────
    resolved = os.path.abspath(output_path)
    fig.savefig(resolved, dpi=150, bbox_inches="tight", facecolor=BG_DARK)
    plt.close(fig)
    return resolved
