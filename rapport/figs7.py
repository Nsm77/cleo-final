"""Figure fishbone (Ishikawa) — le problème central et ses six familles de causes (I.3.3)."""
import os
from mpl import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

# ── Variante du logo pour la couverture encre ─────────────
fc, axc = fig(3.4, 2.6)
fc.patch.set_facecolor("#1F1B16")
axc.set_facecolor("#1F1B16")
axc.set_xlim(0, 10)
axc.set_ylim(0, 10)
box(axc, (1.2, 1.6), 7.6, 6.8, "", fc="#2B2620", ec="#C9A959")
axc.text(5, 6.9, "C", ha="center", va="center", fontsize=44, color="#C9A959",
         family="DejaVu Serif", weight="bold")
axc.text(5, 4.9, "C L É O P Â T R E", ha="center", va="center", fontsize=11, color="#F5EFE2",
         weight="bold", family="DejaVu Serif")
axc.plot([2.6, 7.4], [4.15, 4.15], color="#C9A959", lw=1)
axc.text(5, 3.45, "ESPACE SANTÉ BEAUTÉ", ha="center", va="center", fontsize=7, color="#C9A959")
axc.text(5, 2.7, "EZZAHRA · HAMMAM-LIF", ha="center", va="center", fontsize=5.5, color="#8d8474")
import matplotlib.pyplot as _plt
fc.tight_layout(pad=0.6)
fc.savefig(f"{OUT}/fig01_cover.png", dpi=200, facecolor="#1F1B16")
_plt.close(fc)
print("OK", f"{OUT}/fig01_cover.png")

CAUSES = [
    ("CHIFFRE D'AFFAIRES", "critique",
     ["Invisible sur Google", "Achats hors maison", "Grand Tunis inexploité"]),
    ("STOCK", "majeur",
     ["Inventaire de mémoire", "Ruptures surprises", "Surstocks dormants"]),
    ("PROCESSUS", "majeur",
     ["Commandes sans trace", "Litiges improuvables", "Dossiers non transmissibles"]),
    ("PILOTAGE", "structurant",
     ["Aucun indicateur", "Campagnes non mesurées", "Assortiment à l'aveugle"]),
    ("DONNÉES CLIENT", "structurant",
     ["Pas de fichier client", "Aucun avis collecté", "Fidélisation impossible"]),
    ("CONCURRENCE", "stratégique",
     ["Marketplaces généralistes", "Concurrents en ligne", "Écart qui se creuse"]),
]

SPINE = 3.0
f, ax = fig(6.6, 5.2)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7.9)
title(ax, "Le problème central et ses causes — arête de poisson (synthèse de la critique de l'existant)", fs=8.5)

ax.plot([0.5, 8.0], [SPINE, SPINE], color=INK, lw=2.2)
ax.add_patch(FancyBboxPatch((8.0, SPINE - 0.85), 1.7, 1.7,
                             boxstyle="round,pad=0.02,rounding_size=0.08",
                             fc=RED, ec=INK, lw=1.3))
ax.text(8.85, SPINE, "Croissance\nbridée :\nla maison ne vend\nqu'au comptoir",
        ha="center", va="center", fontsize=6.3, weight="bold", color="white", linespacing=1.3)

xs = [2.0, 4.3, 6.6]
txs = [0.15, 2.95, 5.25]
for (cat, grav, items), x, tx in zip(CAUSES[:3], xs, txs):
    ax.plot([x, x + 1.1], [SPINE, 5.15], color=GOLD, lw=1.6)
    box(ax, (x - 0.05, 5.20), 2.1, 0.66, f"{cat}\n({grav})", fs=6.2, fc=INK, ec=INK,
        tc="white", bold=True)
    for i, it in enumerate(items):
        ax.text(tx, 4.82 - i * 0.36, "•  " + it, ha="left", va="center",
                fontsize=5.3, color=INK)
for (cat, grav, items), x, tx in zip(CAUSES[3:], xs, txs):
    ax.plot([x, x + 1.1], [SPINE, 0.95], color=GOLD, lw=1.6)
    box(ax, (x - 0.05, 0.24), 2.1, 0.66, f"{cat}\n({grav})", fs=6.2, fc=INK, ec=INK,
        tc="white", bold=True)
    for i, it in enumerate(items):
        ax.text(tx, 1.28 + (len(items) - 1 - i) * 0.36, "•  " + it, ha="left",
                va="center", fontsize=5.3, color=INK)

ax.text(0.5, 0.02, "Lecture : chaque arête est documentée en I.3.2 – I.3.3 ; la tête formule le problème que la plateforme doit résoudre.",
        ha="left", va="bottom", fontsize=6.0, color=MUTED, style="italic")
save(f, f"{OUT}/figFISHBONE.png")
print("figs7 done")
