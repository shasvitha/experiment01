"""
Creates the two figures used in the Experiment 1 report:
  fig_design.png  - full-factorial design diagram (Figure 1)
  fig_box.png     - box plots of execution time per condition (Figure 2)

Usage:  python make_plots.py
Requires: matplotlib  (pip install matplotlib)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "DejaVu Sans"

# ------------------------------------------------------------------
# Figure 1: design diagram
# ------------------------------------------------------------------
def make_design_figure(path="fig_design.png"):
    fig, ax = plt.subplots(figsize=(8, 4.3))
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56)

    def box(x, y, w, h, text, fc="#ffffff", fs=8.5, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.2,rounding_size=1",
                                    fc=fc, ec="black", lw=1))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, fontweight="bold" if bold else "normal")

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=1))

    box(28, 47, 44, 7, "Full-factorial design (3 × 3 × 2)",
        fc="#e6e6e6", bold=True, fs=9.5)
    box(2, 31, 28, 10, "Factor A: Algorithm\n(3 levels)\nPassPerItem · UntilNoChange\nWhileNeeded")
    box(36, 31, 28, 10, "Factor B: Input ordering\n(3 levels)\nRandom · Pre-sorted\nReverse-sorted")
    box(70, 31, 28, 10, "Factor C: Array size N\n(2 levels)\n1,000 · 5,000")
    for x in (16, 50, 84):
        arrow(50, 47, x, 41)

    box(28, 17, 44, 8, "18 treatment conditions\n(3 × 3 × 2, fully crossed)", fc="#f2f2f2")
    for x in (16, 50, 84):
        arrow(x, 31, 50, 25)

    box(20, 3, 60, 9,
        "10 replications per condition\n(master-array cloning + JIT warm-up)\n"
        "→ 180 observations · DV: execution time (ms)", fc="#f2f2f2")
    arrow(50, 17, 50, 12)

    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------
# Figure 2: box plots from the five-number summaries
# Values: (min, Q1, median, Q3, max, mean) in ms
# ------------------------------------------------------------------
DATA = {
    ("Random", 1000): {
        "UntilNoChange": (1.8641, 1.8866, 1.9653, 2.0388, 2.2712, 1.9870),
        "WhileNeeded":   (1.2343, 1.2507, 1.2851, 1.2958, 1.4958, 1.2827),
        "PassPerItem":   (1.5892, 1.6472, 1.6705, 1.6929, 1.8960, 1.6951)},
    ("Random", 5000): {
        "UntilNoChange": (53.1104, 54.0182, 55.0617, 55.3030, 74.8119, 56.6504),
        "WhileNeeded":   (33.2988, 34.3368, 34.4719, 35.2150, 35.7932, 34.6721),
        "PassPerItem":   (46.4643, 46.8799, 47.1406, 47.7733, 48.4097, 47.2706)},
    ("Sorted", 1000): {
        "UntilNoChange": (0.0015, 0.0018, 0.0019, 0.0020, 0.0022, 0.0019),
        "WhileNeeded":   (0.0018, 0.0018, 0.0020, 0.0020, 0.0030, 0.0020),
        "PassPerItem":   (0.9801, 1.0015, 1.0232, 1.0365, 1.0688, 1.0223)},
    ("Sorted", 5000): {
        "UntilNoChange": (0.0086, 0.0088, 0.0088, 0.0090, 0.0093, 0.0089),
        "WhileNeeded":   (0.0091, 0.0094, 0.0096, 0.0106, 0.0116, 0.0099),
        "PassPerItem":   (30.9093, 31.2056, 31.4884, 31.9356, 32.3322, 31.5668)},
    ("Reverse", 1000): {
        "UntilNoChange": (2.2840, 2.3102, 2.3347, 2.3535, 2.4333, 2.3411),
        "WhileNeeded":   (1.5996, 1.6003, 1.6159, 1.6230, 1.6283, 1.6128),
        "PassPerItem":   (1.7038, 1.7398, 1.7417, 1.8014, 1.8234, 1.7611)},
    ("Reverse", 5000): {
        "UntilNoChange": (60.8716, 61.1258, 61.2720, 61.4085, 66.2570, 61.7342),
        "WhileNeeded":   (40.1015, 40.1560, 40.2160, 40.8080, 54.9103, 42.5507),
        "PassPerItem":   (45.8858, 46.0786, 46.1899, 46.2700, 61.5648, 47.7884)},
}
COLORS = {"UntilNoChange": "#dcdcdc", "WhileNeeded": "#9e9e9e", "PassPerItem": "#ffffff"}
LABELS = {"UntilNoChange": "Until\nNoChange", "WhileNeeded": "While\nNeeded",
          "PassPerItem": "Pass\nPerItem"}

def make_box_figure(path="fig_box.png"):
    fig, axs = plt.subplots(2, 3, figsize=(8.2, 6.2))
    for r, n in enumerate((5000, 1000)):
        for c, ordering in enumerate(("Random", "Sorted", "Reverse")):
            ax = axs[r][c]
            d = DATA[(ordering, n)]
            algs = list(d)
            stats = [dict(label=LABELS[a], whislo=d[a][0], q1=d[a][1], med=d[a][2],
                          q3=d[a][3], whishi=d[a][4], mean=d[a][5], fliers=[])
                     for a in algs]
            bp = ax.bxp(stats, patch_artist=True, showmeans=True, widths=0.55,
                        meanprops=dict(marker="D", markerfacecolor="white",
                                       markeredgecolor="black", markersize=4),
                        medianprops=dict(color="black", lw=1.5))
            for patch, a in zip(bp["boxes"], algs):
                patch.set_facecolor(COLORS[a])
                patch.set_edgecolor("black")
            if ordering == "Sorted":          # PassPerItem is orders of magnitude slower
                ax.set_yscale("log")
                ax.set_ylabel("Execution time (ms, log scale)", fontsize=8)
            elif c == 0:
                ax.set_ylabel("Execution time (ms)", fontsize=8)
            ax.set_title(f"{ordering}, N = {n:,}", fontsize=9)
            ax.tick_params(labelsize=7)
            ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_design_figure()
    make_box_figure()
    print("Saved fig_design.png and fig_box.png")