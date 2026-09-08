"""Helpers matplotlib pour générer les figures du rapport (style unifié)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch, Circle, Rectangle
import matplotlib.patheffects as pe

INK = "#2B2620"
GOLD = "#8C6924"
GOLD_L = "#C9A959"
PAPER = "#FFFFFF"
SHADE = "#F7F3EB"
STONE = "#D8CFBE"
MUTED = "#6E685A"
BLUE = "#3E5C76"
BLUE_L = "#DCE6EF"
GREEN = "#5B7A5E"
GREEN_L = "#E2EADF"
RED = "#A34A3E"
RED_L = "#F2DEDB"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": STONE,
})


def fig(w_in=6.6, h_in=4.0):
    f, ax = plt.subplots(figsize=(w_in, h_in), dpi=200)
    f.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    ax.set_axis_off()
    return f, ax


def save(f, path):
    f.tight_layout(pad=0.6)
    f.savefig(path, dpi=200, facecolor=PAPER)
    plt.close(f)
    print("OK", path)


def box(ax, xy, w, h, text, fs=8.5, fc=PAPER, ec=INK, tc=INK, bold=False, align="center", ls="-", lw=1.1, alpha=1.0, fontsize2=None):
    x, y = xy
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.03",
                       fc=fc, ec=ec, lw=lw, ls=ls, alpha=alpha)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha=align, va="center", fontsize=fs,
            color=tc, weight="bold" if bold else "normal", wrap=True, linespacing=1.35)
    return p


def ellipse_node(ax, xy, w, h, text, fs=8, fc=BLUE_L, ec=BLUE, tc=INK):
    x, y = xy
    e = Ellipse((x + w / 2, y + h / 2), w, h, fc=fc, ec=ec, lw=1.2)
    ax.add_patch(e)
    ax.text(x + w / 2, y + h / 2, "«use case»\n" + text if False else text, ha="center", va="center",
            fontsize=fs, color=tc, wrap=True, linespacing=1.3)
    return e


def actor(ax, x, y, label, fs=8.5, scale=1.0):
    # stick figure
    s = scale
    head = Circle((x, y + 0.62 * s), 0.11 * s, fc=PAPER, ec=INK, lw=1.3)
    ax.add_patch(head)
    ax.plot([x, x], [y + 0.51 * s, y + 0.10 * s], color=INK, lw=1.3)
    ax.plot([x - 0.20 * s, x + 0.20 * s], [y + 0.38 * s, y + 0.38 * s], color=INK, lw=1.3)
    ax.plot([x, x - 0.14 * s], [y + 0.10 * s, y - 0.12 * s], color=INK, lw=1.3)
    ax.plot([x, x + 0.14 * s], [y + 0.10 * s, y - 0.12 * s], color=INK, lw=1.3)
    ax.text(x, y - 0.22 * s, label, ha="center", va="top", fontsize=fs, color=INK, style="italic",
            wrap=True)


def arrow(ax, p1, p2, label="", fs=7.5, color=INK, ls="-", lw=1.1, rad=0.0, style="-|>", shrink=2):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, color=color, lw=lw, ls=ls,
                        connectionstyle=f"arc3,rad={rad}", shrinkA=shrink, shrinkB=shrink,
                        mutation_scale=11)
    ax.add_patch(a)
    if label:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        t = ax.text(mx, my + 0.06, label, ha="center", va="bottom", fontsize=fs, color=color,
                    bbox=dict(fc=PAPER, ec="none", pad=1.2))
    return a


def title(ax, text, fs=11):
    ax.text(0.5, 0.97, text, ha="center", va="top", fontsize=fs, weight="bold", color=INK,
            transform=ax.transAxes)
