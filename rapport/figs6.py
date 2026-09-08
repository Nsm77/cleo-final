"""Figures prestige : tableau des chiffres-clés + feuille de route du projet."""
import os
from mpl import *
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

# ══ Chiffres-clés (conclusion) ═══════════════════════════
f, ax = fig(6.6, 3.9)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.text(5, 9.4, "Le projet en chiffres", ha="center", va="center", fontsize=11,
        weight="bold", color=INK)
stats = [("24", "récits livrés", "100 % démontrés"),
         ("81", "produits", "16 marques · 7 univers"),
         ("24", "tables", "10 énumérations"),
         ("7", "statuts", "cycle de vie"),
         ("4+1", "sprints", "2 releases"),
         ("0", "dette critique", "qualité tenue")]
for j, (n, t1, t2) in enumerate(stats):
    x = 0.15 + (j % 3) * 3.28
    y = 4.85 if j < 3 else 0.65
    ax.add_patch(FancyBboxPatch((x, y), 3.0, 3.6,
                                boxstyle="round,pad=0.02,rounding_size=0.18",
                                fc="#2B2620", ec="#2B2620", lw=0))
    ax.add_patch(FancyBboxPatch((x, y + 3.25), 3.0, 0.35,
                                boxstyle="round,pad=0.02,rounding_size=0.18",
                                fc=GOLD, ec=GOLD, lw=0))
    ax.add_patch(FancyBboxPatch((x, y + 3.25), 3.0, 0.18, boxstyle="square,pad=0",
                                fc=GOLD, ec="none"))
    ax.text(x + 1.5, y + 2.25, n, ha="center", va="center", fontsize=26,
            weight="bold", color="white")
    ax.text(x + 1.5, y + 1.15, t1, ha="center", va="center", fontsize=8.5,
            weight="bold", color="#C9A959")
    ax.text(x + 1.5, y + 0.55, t2, ha="center", va="center", fontsize=6.5, color="#B9AC93")
save(f, f"{OUT}/figKPI.png")

# ══ Feuille de route (sprint 0) ══════════════════════════
f, ax = fig(6.6, 4.4)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.text(5, 9.4, "Feuille de route — du cadrage à la soutenance", ha="center",
        va="center", fontsize=11, weight="bold", color=INK)
ax.plot([0.3, 8.8], [5.6, 5.6], color=GOLD, lw=2.5, solid_capstyle="round", zorder=1)
steps = [("S0", "Cadrage", "acteurs · besoins\nbacklog · stack"),
         ("S1", "Socle", "comptes · rôles\ndashboard"),
         ("S2", "Commerce", "catalogue · stock\ncommandes"),
         ("S3", "Relation", "avis · support"),
         ("S4", "Finition", "recherche · Docker"),
         ("★", "Soutenance", "démo · jury")]
for j, (n, t1, t2) in enumerate(steps):
    x = 0.75 + j * 1.5
    c = FancyBboxPatch((x - 0.52, 5.08), 1.04, 1.04,
                       boxstyle="round,pad=0.02,rounding_size=0.52",
                       fc="#2B2620", ec=GOLD, lw=1.8, zorder=2)
    ax.add_patch(c)
    ax.text(x, 5.6, n, ha="center", va="center", fontsize=10, weight="bold",
            color="white", zorder=3)
    ax.text(x, 4.55, t1, ha="center", va="center", fontsize=8, weight="bold", color=INK)
    for k, line in enumerate(t2.split("\n")):
        ax.text(x, 3.95 - k * 0.5, line, ha="center", va="center", fontsize=6.5, color=MUTED)
box(ax, (0.3, 1.15), 6.1, 1.15, "Release 1 — cœur marchand (S1 + S2) : on peut réellement acheter",
    fs=7, fc=SHADE, ec=GOLD)
box(ax, (6.6, 1.15), 3.1, 1.15, "Release 2 (S3 + S4)\nplateforme complète",
    fs=7, fc=SHADE, ec=GOLD)
save(f, f"{OUT}/figROADMAP.png")
print("figs6 done")
