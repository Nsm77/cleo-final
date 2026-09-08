"""Figures 1-22 : chapitres I et II (logo, organigramme, Scrum, UC général, logos tech, architectures)."""
import os
from mpl import *
from matplotlib.patches import FancyBboxPatch, Ellipse

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)

# ── Fig 1 : logo Cléopâtre ──────────────────────────────────
f, ax = fig(3.4, 2.6)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
box(ax, (1.2, 1.6), 7.6, 6.8, "", fc="#2B2620", ec="#2B2620")
ax.text(5, 6.9, "C", ha="center", va="center", fontsize=44, color="#C9A959",
        family="DejaVu Serif", weight="bold")
ax.text(5, 4.9, "C L É O P Â T R E", ha="center", va="center", fontsize=11, color="#F5EFE2",
        weight="bold", family="DejaVu Serif")
ax.plot([2.6, 7.4], [4.15, 4.15], color="#C9A959", lw=1)
ax.text(5, 3.45, "ESPACE SANTÉ BEAUTÉ", ha="center", va="center", fontsize=7, color="#C9A959")
ax.text(5, 2.7, "EZZAHRA · HAMMAM-LIF", ha="center", va="center", fontsize=5.5, color="#8d8474")
save(f, f"{OUT}/fig01_logo.png")

# ── Fig 2 : organigramme service digital ────────────────────
f, ax = fig(6.6, 3.6)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
title(ax, "Organigramme du service digital — Parapharmacie Cléopâtre")
box(ax, (3.4, 7.3), 3.2, 1.1, "Direction générale", bold=True, fc="#2B2620", tc="white", fs=8.5)
box(ax, (0.3, 4.9), 3.0, 1.1, "Responsable\ndigital & e-commerce", fc=GOLD_L, ec=GOLD, fs=7.8)
box(ax, (3.55, 4.9), 3.0, 1.1, "Pharmacien référent\n(contenu & conseil)", fc=SHADE, ec=MUTED, fs=7.8)
box(ax, (6.8, 4.9), 3.0, 1.1, "Responsable\nboutiques", fc=SHADE, ec=MUTED, fs=7.8)
box(ax, (0.3, 2.5), 3.0, 1.1, "Développeur\nfull-stack (stagiaire)", fc=BLUE_L, ec=BLUE, fs=7.8)
box(ax, (3.55, 2.5), 3.0, 1.1, "Préparateur\ncommandes web", fc=SHADE, ec=MUTED, fs=7.8)
box(ax, (6.8, 2.5), 3.0, 1.1, "Chargé(e) de\nrelation client", fc=SHADE, ec=MUTED, fs=7.8)
for x in (1.8, 5.05, 8.3):
    arrow(ax, (5, 7.3), (x, 6.0), lw=1.0)
arrow(ax, (1.8, 4.9), (1.8, 3.6), lw=1.0)
arrow(ax, (5.05, 4.9), (5.05, 3.6), lw=1.0)
arrow(ax, (8.3, 4.9), (8.3, 3.6), lw=1.0)
save(f, f"{OUT}/fig02_orga.png")

# ── Fig 3 : processus Scrum ─────────────────────────────────
f, ax = fig(6.6, 4.0)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
title(ax, "Le processus Scrum")
box(ax, (0.2, 4.2), 1.9, 2.2, "Backlog\ndu produit", fc="#2B2620", tc="white", bold=True, fs=8)
box(ax, (2.6, 6.9), 2.1, 1.2, "Planification\ndu sprint", fc=GOLD_L, ec=GOLD, fs=7.5)
box(ax, (5.1, 6.9), 2.1, 1.2, "Mêlée\nquotidienne", fc=SHADE, ec=MUTED, fs=7.5)
box(ax, (7.6, 6.9), 2.1, 1.2, "Revue +\nRétrospective", fc=SHADE, ec=MUTED, fs=7.5)
box(ax, (2.6, 4.2), 4.6, 1.6, "Sprint (2 semaines) — Backlog de sprint", fc=BLUE_L, ec=BLUE, fs=8)
box(ax, (7.6, 4.2), 2.1, 1.6, "Incrément\npotentiellement\nlivrable", fc=GREEN_L, ec=GREEN, fs=7.5)
box(ax, (2.6, 2.3), 2.1, 1.0, "Product Owner", fc=PAPER, ec=GOLD, fs=7.5)
box(ax, (5.1, 2.3), 2.1, 1.0, "Scrum Master", fc=PAPER, ec=GOLD, fs=7.5)
box(ax, (7.6, 2.3), 2.1, 1.0, "Équipe de dev.", fc=PAPER, ec=GOLD, fs=7.5)
arrow(ax, (2.1, 5.3), (2.6, 5.3))
arrow(ax, (4.7, 6.9), (4.7, 5.8))
arrow(ax, (6.15, 6.9), (6.15, 5.8))
arrow(ax, (8.65, 6.9), (8.65, 5.8))
arrow(ax, (7.2, 5.0), (7.6, 5.0))
arrow(ax, (8.65, 4.2), (8.65, 3.3), ls="--", color=MUTED)
arrow(ax, (7.6, 2.8), (2.6, 2.8), ls="--", color=MUTED)
arrow(ax, (2.1, 4.2), (2.1, 2.8), ls="--", color=MUTED)
ax.text(5.1, 1.55, "Boucle d'amélioration continue", ha="center", fontsize=7.5, color=MUTED, style="italic")
save(f, f"{OUT}/fig03_scrum.png")

# ── helper : diagramme de cas d'utilisation ─────────────────
def uc_diagram(path, title_t, actors_left, actors_right, uses, links, w_in=6.6, h_in=4.4):
    f, ax = fig(w_in, h_in)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    title(ax, title_t)
    # boundary
    bx, bw = 2.9, 5.0
    by, bh = 0.7, 8.0
    ax.add_patch(FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="#FBF8F1", ec=MUTED, lw=1.1, ls="--"))
    ax.text(bx + bw / 2, by + bh - 0.15, "Plateforme Cléopâtre", ha="center", va="top", fontsize=7.5,
            color=MUTED, style="italic")
    pos = {}
    n = len(uses)
    for i, u in enumerate(uses):
        y = by + bh - 1.1 - i * ((bh - 1.6) / max(1, n - 1 if n > 1 else 1)) - 0.45 if n > 1 else by + bh / 2 - 0.45
        ellipse_node(ax, (bx + 0.55, y), bw - 1.1, 0.9, u, fs=7.6)
        pos[u] = (bx + 0.55 + (bw - 1.1) / 2, y + 0.45)
    # actors
    apos = {}
    for j, a in enumerate(actors_left):
        y = 8.0 - j * 1.6
        actor(ax, 1.0, y - 0.5, a, fs=7.4, scale=0.85)
        apos[a] = (1.2, y - 0.15)
    for j, a in enumerate(actors_right):
        y = 8.0 - j * 1.6
        actor(ax, 9.1, y - 0.5, a, fs=7.4, scale=0.85)
        apos[a] = (8.9, y - 0.15)
    for a, u in links:
        if a in apos and u in pos:
            p1, p2 = apos[a], pos[u]
            if p1[0] < p2[0]:
                arrow(ax, p1, (bx + 0.5, p2[1]), style="-", lw=0.9, color=MUTED)
            else:
                arrow(ax, p1, (bx + bw - 0.5, p2[1]), style="-", lw=0.9, color=MUTED)
    save(f, path)

# ── Fig 4 : UC général ──────────────────────────────────────
uc_diagram(f"{OUT}/fig04_uc_general.png", "Diagramme de cas d'utilisation général",
    ["Visiteur", "Client", "Pharmacien\nconseil"],
    ["Support\nclient", "Administrateur"],
    ["Consulter le catalogue", "Gérer le panier", "Passer commande",
     "Suivre ses commandes", "Donner son avis", "Administrer la plateforme"],
    [("Visiteur", "Consulter le catalogue"), ("Visiteur", "Gérer le panier"),
     ("Client", "Consulter le catalogue"), ("Client", "Gérer le panier"),
     ("Client", "Passer commande"), ("Client", "Suivre ses commandes"),
     ("Client", "Donner son avis"), ("Pharmacien\nconseil", "Donner son avis"),
     ("Administrateur", "Administrer la plateforme"),
     ("Support\nclient", "Suivre ses commandes")],
    h_in=4.8)

# ── Figs 5-18 : logos techno ────────────────────────────────
LOGOS = [
    ("05_drawio", "draw.io", "Modélisation", "#E88B1D", "di"),
    ("06_staruml", "StarUML", "Modélisation UML", "#3E5C76", "SU"),
    ("07_vscode", "Visual Studio Code", "Éditeur de code", "#007ACC", "VS"),
    ("08_nextjs", "Next.js 16", "Framework full-stack", "#111111", "N"),
    ("09_react", "React 19", "Bibliothèque UI", "#0E7490", "Re"),
    ("10_typescript", "TypeScript", "Langage typé", "#3178C6", "TS"),
    ("11_tailwind", "Tailwind CSS", "Framework CSS", "#0E7490", "TW"),
    ("12_nodejs", "Node.js 22", "Exécution serveur", "#2F7D32", "No"),
    ("13_postgres", "PostgreSQL 18", "Base de données", "#336791", "PG"),
    ("14_drizzle", "Drizzle ORM", "Accès données", "#4D7C0F", "Dz"),
    ("15_zod", "Zod", "Validation", "#3E63DD", "Z"),
    ("16_docker", "Docker", "Conteneurisation", "#2496ED", "Do"),
    ("17_github", "Git & GitHub", "Versionnement", "#111111", "Gh"),
    ("18_framer", "Framer Motion", "Animations", "#B026A2", "FM"),
]
for code, name, sub, color, mono in LOGOS:
    f, ax = fig(2.4, 2.0)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.add_patch(FancyBboxPatch((3.1, 3.6), 3.8, 3.8, boxstyle="round,pad=0.02,rounding_size=0.5",
                                fc=color, ec=color, lw=0))
    ax.text(5, 5.5, mono, ha="center", va="center", fontsize=22, color="white", weight="bold")
    ax.text(5, 2.6, name, ha="center", va="center", fontsize=9.5, color=INK, weight="bold")
    ax.text(5, 1.6, sub, ha="center", va="center", fontsize=7.5, color=MUTED)
    save(f, f"{OUT}/fig{code}.png")

# ── Fig 19 : diagramme de déploiement ───────────────────────
f, ax = fig(6.6, 4.2)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
title(ax, "Diagramme de déploiement — architecture physique")
box(ax, (0.2, 5.6), 2.6, 2.6, "«device»\nNavigateur client\n(PC / mobile)", fs=7.5, fc=GREEN_L, ec=GREEN)
box(ax, (3.5, 5.6), 3.0, 2.6, "«device»\nServeur applicatif\nNext.js + Node.js", fs=7.5, fc=BLUE_L, ec=BLUE, bold=True)
box(ax, (7.2, 5.6), 2.6, 2.6, "«device»\nServeur PostgreSQL\n(données)", fs=7.5, fc=GOLD_L, ec=GOLD)
box(ax, (3.5, 2.6), 3.0, 1.6, "Conteneur Docker\n« cleo-web »", fs=7.5, fc=PAPER, ec=INK, ls="--")
box(ax, (7.2, 2.6), 2.6, 1.6, "Conteneur Docker\n« cleo-db »", fs=7.5, fc=PAPER, ec=INK, ls="--")
box(ax, (0.2, 2.6), 2.6, 1.6, "CDN / reverse proxy\n(HTTPS, cache)", fs=7.5, fc=SHADE, ec=MUTED)
arrow(ax, (2.8, 6.9), (3.5, 6.9), "HTTPS", fs=7)
arrow(ax, (6.5, 6.9), (7.2, 6.9), "TCP 5432", fs=7)
arrow(ax, (1.5, 5.6), (1.5, 4.2), style="-", color=MUTED)
arrow(ax, (5.0, 5.6), (5.0, 4.2), style="-", color=MUTED)
arrow(ax, (8.5, 5.6), (8.5, 4.2), style="-", color=MUTED)
arrow(ax, (2.8, 3.4), (3.5, 3.4), style="-", color=MUTED)
arrow(ax, (6.5, 3.4), (7.2, 3.4), style="-", color=MUTED)
ax.text(5, 1.5, "Stéréotypes UML : «device» = nœud matériel, «artifact» déployé dans un conteneur Docker.",
        ha="center", fontsize=7, color=MUTED, style="italic")
save(f, f"{OUT}/fig19_deploiement.png")

# ── Fig 20 : architecture logicielle ────────────────────────
f, ax = fig(6.6, 4.4)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
title(ax, "Architecture logicielle — monolithe modulaire Next.js")
box(ax, (0.5, 7.6), 9.0, 0.9, "PRÉSENTATION — Pages & composants React (App Router : vitrine « site » + back-office « admin »)", fs=7.3, fc=GREEN_L, ec=GREEN)
box(ax, (0.5, 6.2), 4.4, 1.1, "ACTIONS SERVEUR — Auth · Boutique · Panier · Commande", fs=7.3, fc=BLUE_L, ec=BLUE)
box(ax, (5.1, 6.2), 4.4, 1.1, "ACTIONS ADMIN — Catalogue · Stock · Promos · Support", fs=7.3, fc=BLUE_L, ec=BLUE)
box(ax, (0.5, 4.8), 2.9, 1.1, "SERVICES MÉTIER\nPanier · Promos · Commandes", fs=7.3, fc=GOLD_L, ec=GOLD)
box(ax, (3.6, 4.8), 2.9, 1.1, "SÉCURITÉ\nSessions · Zod · Rate-limit", fs=7.3, fc=GOLD_L, ec=GOLD)
box(ax, (6.7, 4.8), 2.8, 1.1, "RÉFÉRENTIELS\nArgent · Tunisie · I18n", fs=7.3, fc=GOLD_L, ec=GOLD)
box(ax, (0.5, 3.4), 9.0, 1.1, "PERSISTANCE — Drizzle ORM + PostgreSQL (23 tables, contraintes, index, transactions)", fs=7.3, fc=SHADE, ec=MUTED)
box(ax, (0.5, 2.0), 9.0, 1.1, "SOCLE — Next.js 16 · React 19 · Node.js 22 · Docker", fs=7.3, fc="#2B2620", tc="white", ec="#2B2620")
for y1, y2 in [(7.6, 7.3), (6.2, 5.9), (4.8, 4.5), (3.4, 3.1)]:
    pass
arrow(ax, (5, 7.6), (5, 7.32), style="-", color=MUTED)
arrow(ax, (2.7, 6.2), (2.7, 5.92), style="-", color=MUTED)
arrow(ax, (7.3, 6.2), (7.3, 5.92), style="-", color=MUTED)
arrow(ax, (5, 4.8), (5, 4.52), style="-", color=MUTED)
arrow(ax, (5, 3.4), (5, 3.12), style="-", color=MUTED)
save(f, f"{OUT}/fig20_archilogicielle.png")

# ── Fig 21 : paquetages ─────────────────────────────────────
f, ax = fig(6.6, 4.2)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
title(ax, "Diagramme de paquetages")
def pkg(ax, x, y, w, h, name, items, fc=PAPER):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.01", fc=fc, ec=INK, lw=1.1))
    ax.add_patch(FancyBboxPatch((x, y + h), w * 0.42, 0.42, boxstyle="square,pad=0.01", fc=fc, ec=INK, lw=1.1))
    ax.text(x + w * 0.21, y + h + 0.21, name, ha="center", va="center", fontsize=7.6, weight="bold")
    for i, it in enumerate(items):
        ax.text(x + 0.15, y + h - 0.35 - i * 0.32, "• " + it, ha="left", va="center", fontsize=6.8, color=INK)
pkg(ax, 0.3, 4.6, 3.0, 2.6, "app/(site)", ["page.tsx — accueil", "boutique · produit", "panier · commande", "compte · suivi"], GREEN_L)
pkg(ax, 3.55, 4.6, 3.0, 2.6, "app/admin", ["dashboard", "commandes · stock", "clients · support", "journal · audit"], BLUE_L)
pkg(ax, 6.8, 4.6, 3.0, 2.6, "components", ["catalog · checkout", "shell · motion", "ui · icons"], SHADE)
pkg(ax, 0.3, 1.3, 3.0, 2.2, "actions", ["auth · shop", "checkout", "admin"], GOLD_L)
pkg(ax, 3.55, 1.3, 3.0, 2.2, "lib", ["auth · money · orders", "promotions · catalog", "validation · rate-limit"], GOLD_L)
pkg(ax, 6.8, 1.3, 3.0, 2.2, "db", ["schema.ts — 23 tables", "seed.ts — démo"], "#EDE6D6")
arrow(ax, (1.8, 4.6), (1.8, 3.55), ls="--", color=MUTED)
arrow(ax, (5.05, 4.6), (5.05, 3.55), ls="--", color=MUTED)
arrow(ax, (8.3, 4.6), (8.3, 3.55), ls="--", color=MUTED)
arrow(ax, (3.55, 2.4), (3.3, 2.4), style="-", color=MUTED)
arrow(ax, (6.8, 2.4), (6.55, 2.4), style="-", color=MUTED)
ax.text(5, 0.7, "Dépendances : présentation → actions → lib → db (jamais l'inverse).", ha="center", fontsize=7, color=MUTED, style="italic")
save(f, f"{OUT}/fig21_paquetage.png")

# ── Fig 22 : cycle de vie Server Action ─────────────────────
f, ax = fig(6.6, 3.8)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
title(ax, "Cycle de vie d'une Server Action (ex. passer commande)")
steps = [("Client\n(click)", GREEN_L), ("Vérifications\norigine + quota", GOLD_L), ("Validation\nZod", GOLD_L),
         ("Transaction\nPostgreSQL", BLUE_L), ("Revalidation\ndu cache", SHADE), ("Réponse\ntypée", GREEN_L)]
x = 0.25
for i, (s, c) in enumerate(steps):
    box(ax, (x, 4.6), 1.42, 1.7, s, fs=7.2, fc=c, ec=MUTED if c == SHADE else INK)
    if i < len(steps) - 1:
        arrow(ax, (x + 1.42, 5.45), (x + 1.65, 5.45), lw=1.2)
    x += 1.65
box(ax, (0.25, 2.5), 4.6, 1.2, "Échec ⇒ message d'erreur en français, sans fuite technique", fs=7.2, fc=RED_L, ec=RED)
box(ax, (5.05, 2.5), 4.6, 1.2, "Idempotence : double clic ⇒ une seule commande", fs=7.2, fc=BLUE_L, ec=BLUE)
save(f, f"{OUT}/fig22_serveraction.png")

print("figs1 done")
