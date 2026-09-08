"""Figures 63-86 : sprints 3 et 4 (avis, support, recherche, journal, Docker, vitrine finale)."""
import os
from mpl import *
from figs1 import uc_diagram
from figs2 import (seq_diagram, class_box, browser, mtext, mbtn, mfield, mtable,
                   msidebar, mtopnav, M_SUB, M_TXT, M_ACC, M_LINE, M_BTN)
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)

# ── Figs 63-65 : UC sprint 3 ───────────────────────────────
uc_diagram(f"{OUT}/fig63_uc_reviews.png", "Diagramme du cas d'utilisation « Gérer les avis clients »",
    ["Client"], ["Équipe (support/admin)"],
    ["Déposer un avis", "Modérer un avis", "Répondre à un avis", "Voir la note moyenne"],
    [("Client", "Déposer un avis"), ("Client", "Voir la note moyenne"),
     ("Équipe (support/admin)", "Modérer un avis"), ("Équipe (support/admin)", "Répondre à un avis")])
uc_diagram(f"{OUT}/fig64_uc_tickets.png", "Diagramme du cas d'utilisation « Gérer les réclamations »",
    ["Client / Visiteur"], ["Support"],
    ["Créer une réclamation", "Consulter ses tickets", "Voir la file des tickets", "Clôturer un ticket"],
    [("Client / Visiteur", "Créer une réclamation"), ("Client / Visiteur", "Consulter ses tickets"),
     ("Support", "Voir la file des tickets"), ("Support", "Clôturer un ticket")])
uc_diagram(f"{OUT}/fig65_uc_replies.png", "Diagramme du cas d'utilisation « Gérer les réponses »",
    ["Support"], [],
    ["Rédiger une réponse", "Répondre et clôturer", "Rouvrir un ticket"],
    [("Support", "Rédiger une réponse"), ("Support", "Répondre et clôturer"), ("Support", "Rouvrir un ticket")])

# ── Fig 66 : classes sprint 3 ──────────────────────────────
f, ax = fig(6.6, 4.0)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Diagramme de classes — sprint 3 (relation client)")
class_box(ax, 0.4, 4.6, 4.4, 3.9, "Review",
    ["+ productId FK, userId FK?", "+ authorName, rating 1-5", "+ title?, body", "+ status : enum", "+ reply? : text"],
    ["+ approve() / reject()"], GREEN_L)
class_box(ax, 5.3, 4.6, 4.4, 3.9, "SupportTicket",
    ["+ userId FK?, email, name", "+ subject, message", "+ reply? : text", "+ status : enum", "+ orderNumber?"],
    ["+ answerAndClose()"], BLUE_L)
box(ax, (0.4, 2.2), 4.4, 1.5, "Agrégation atomique :\nmodération + recalcul note ⇒ même transaction", fs=7.2, fc=PAPER, ec=INK, ls="--")
box(ax, (5.3, 2.2), 4.4, 1.5, "Cycle ouvert → répondu → clos\nnotification client à la réponse", fs=7.2, fc=PAPER, ec=INK, ls="--")
save(f, f"{OUT}/fig66_classes_s3.png")

# ── Figs 67-68 : séquences sprint 3 ────────────────────────
seq_diagram(f"{OUT}/fig67_seq_moderate.png", "Diagramme de séquence « Modérer un avis »",
    ["Staff", "File /admin/avis", "moderateReview", "PostgreSQL"],
    [(0, 1, "Approuver / Rejeter (+ réponse)", False), (1, 2, "moderateReviewAction()", False),
     (2, 2, "requireStaff()", False), (2, 3, "BEGIN : UPDATE review", False),
     (2, 3, "re-agrégation AVG + COUNT", False), (2, 3, "UPDATE product.note", False),
     (3, 2, "COMMIT + audit", True), (2, 1, "ok : avis publié", True)])
seq_diagram(f"{OUT}/fig68_seq_ticket.png", "Diagramme de séquence « Traiter une réclamation »",
    ["Client", "Form. contact", "createTicket", "Support"],
    [(0, 1, "décrire le problème", False), (1, 2, "createTicketAction(form)", False),
     (2, 2, "quota anti-spam + Zod", False), (2, 3, "ticket « ouvert » en file", False),
     (3, 3, "replyTicketAction() + clôture", False), (3, 0, "réponse envoyée", True)])

# ── Figs 69-71 : interfaces sprint 3 ───────────────────────
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/avis"); msidebar(ax, ["Vue d'ensemble", "Produits", "Avis clients", "Support"], 2)
mtext(ax, 2.5, 8.0, "Avis clients", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "4 en attente · note moyenne boutique : 4,6 / 5", fs=6.8, color=M_SUB)
mtable(ax, 2.5, 6.35, 7.15, ["Produit", "Auteur", "Note", "Extrait", ""],
       [["Anthelios Fluide", "Amira B.", "★★★★★", "Texture parfaite…", "◉"],
        ["Effaclar Duo+", "Mehdi T.", "★★★★☆", "Efficace et doux…", "◉"],
        ["Huile Prodigieuse", "Salma R.", "★★★☆☆", "Bien mais parfumé…", "◉"]],
       colw=[1.7, 1.1, 0.9, 1.95, 0.5])
ax.add_patch(FancyBboxPatch((2.5, 3.15), 7.15, 1.35, boxstyle="round,pad=0.02,rounding_size=0.1", fc="#F4F0E8", ec=M_LINE, lw=0.9))
mtext(ax, 2.7, 4.2, "Avis sélectionné — réponse de la maison (optionnel) :", fs=6.5, bold=True)
mtext(ax, 2.7, 3.85, "« Merci Amira ! Pour optimiser la protection, renouvelez l'application… »", fs=6.2, color=M_SUB)
mbtn(ax, 2.7, 3.3, 1.4, 0.42, "Approuver", fs=6)
mbtn(ax, 4.25, 3.3, 1.2, 0.42, "Rejeter", primary=False, fs=6)
save(f, f"{OUT}/fig69_reviews.png")

f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/support"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Support", "Recherches"], 2)
mtext(ax, 2.5, 8.0, "Support — réclamations", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "3 tickets ouverts · délai de réponse affiché : sous 24 h ouvrées", fs=6.8, color=M_SUB)
mtable(ax, 2.5, 6.35, 7.15, ["Sujet", "Client", "Commande", "Statut", ""],
       [["Colis en retard ?", "Rim H.", "CL-260904…", "Ouvert", "Ouvrir"],
        ["Produit reçu abîmé", "Khaled M.", "CL-260902…", "Ouvert", "Ouvrir"],
        ["Question routine peau", "Yasmine K.", "—", "Répondu", "Ouvrir"]],
       colw=[1.8, 1.2, 1.3, 1.0, 0.6])
mtext(ax, 2.5, 3.9, "Chaque ticket garde sa commande liée, son historique et sa réponse envoyée.", fs=6.2, color=M_SUB, italic=True)
save(f, f"{OUT}/fig70_tickets.png")

f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/support/7"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Support"], 2)
mtext(ax, 2.5, 8.0, "Ticket n°7 — Colis en retard ?", fs=9.5, bold=True)
mtext(ax, 2.5, 7.6, "Rim H. · rim.h@mail.tn · commande CL-260904-T2V7 · ouvert il y a 3 h", fs=6.5, color=M_SUB)
ax.add_patch(FancyBboxPatch((2.5, 6.1), 7.0, 1.1, boxstyle="round,pad=0.02,rounding_size=0.1", fc="white", ec=M_LINE, lw=0.9))
mtext(ax, 2.7, 6.85, "« Bonjour, mon colis devait arriver hier selon le suivi… »", fs=6.4)
mfield(ax, 2.5, 4.7, 7.0, 1.0, "Réponse de l'équipe", "Bonjour Rim, votre colis est au dépôt de Ben Arous…")
mbtn(ax, 2.5, 3.85, 2.0, 0.5, "Répondre et clôturer", fs=6.2)
mbtn(ax, 4.7, 3.85, 1.7, 0.5, "Répondre", primary=False, fs=6.2)
save(f, f"{OUT}/fig71_ticket_reply.png")

# ── Figs 72-74 : UC sprint 4 ───────────────────────────────
uc_diagram(f"{OUT}/fig72_uc_search.png", "Diagramme du cas d'utilisation « Rechercher un produit »",
    ["Visiteur / Client"], ["Administrateur"],
    ["Recherche instantanée", "Filtrer par facettes", "Voir les suggestions", "Analyser les recherches"],
    [("Visiteur / Client", "Recherche instantanée"), ("Visiteur / Client", "Filtrer par facettes"),
     ("Visiteur / Client", "Voir les suggestions"), ("Administrateur", "Analyser les recherches")])
uc_diagram(f"{OUT}/fig73_uc_guest.png", "Diagramme du cas d'utilisation « Suivre une commande en invité »",
    ["Acheteur invité"], [],
    ["Ouvrir le lien privé", "Voir le détail de commande", "Voir la timeline logistique"],
    [("Acheteur invité", "Ouvrir le lien privé"), ("Acheteur invité", "Voir le détail de commande"),
     ("Acheteur invité", "Voir la timeline logistique")])
uc_diagram(f"{OUT}/fig74_uc_journal.png", "Diagramme du cas d'utilisation « Gérer le journal »",
    ["Client / Visiteur"], ["Administrateur"],
    ["Lire un article", "Publier un article", "Modifier / dépublier"],
    [("Client / Visiteur", "Lire un article"), ("Administrateur", "Publier un article"),
     ("Administrateur", "Modifier / dépublier")])

# ── Fig 75 : classes sprint 4 ──────────────────────────────
f, ax = fig(6.6, 4.0)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Diagramme de classes — sprint 4 (recherche & contenu)")
class_box(ax, 0.4, 4.6, 4.4, 3.9, "Article",
    ["+ slug, title, excerpt", "+ body : text", "+ image?, tag?", "+ readMinutes", "+ isPublished, publishedAt"],
    ["+ publish() / unpublish()"], GREEN_L)
class_box(ax, 5.3, 4.6, 4.4, 3.9, "SearchEvent",
    ["+ query (minuscules)", "+ resultsCount : int", "+ userId?, createdAt"], None, BLUE_L)
box(ax, (0.4, 2.2), 4.4, 1.5, "Journal : contenu éditorial\nrédigé avec les pharmaciens", fs=7.2, fc=PAPER, ec=INK, ls="--")
box(ax, (5.3, 2.2), 4.4, 1.5, "Télémétrie : requêtes sans\nrésultat ⇒ idées d'assortiment", fs=7.2, fc=PAPER, ec=INK, ls="--")
save(f, f"{OUT}/fig75_classes_s4.png")

# ── Figs 76-77 : séquences sprint 4 ────────────────────────
seq_diagram(f"{OUT}/fig76_seq_search.png", "Diagramme de séquence « Recherche instantanée »",
    ["Visiteur", "Barre de recherche", "/api/search", "PostgreSQL"],
    [(0, 1, "taper « anth » (≥ 2 lettres)", False), (1, 2, "GET /api/search?q=anth", False),
     (2, 2, "quota 30 req/min", False), (2, 3, "ILIKE nom + marque (top 6)", False),
     (3, 2, "6 suggestions", True), (2, 1, "JSON + log search_event", True),
     (1, 0, "liste déroulante immédiate", True)])
seq_diagram(f"{OUT}/fig77_seq_guest.png", "Diagramme de séquence « Suivi invité par clé d'accès »",
    ["Invité", "Page /suivi", "loadOrder", "PostgreSQL"],
    [(0, 1, "ouvrir le lien ?k=clé", False), (1, 2, "loadOrder(number, key)", False),
     (2, 3, "SELECT order by number", False), (3, 2, "order + accessKey", True),
     (2, 2, "safeEqual(clé) temps constant", False), (2, 1, "order / refus 404", True),
     (1, 0, "détail + timeline", True)])

# ── Figs 78-82 : interfaces sprint 4 ───────────────────────
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/recherche?q=solaire"); mtopnav(ax)
mfield(ax, 0.5, 6.55, 6.0, 0.55, "", "solaire")
mtext(ax, 0.5, 6.05, "12 résultats · triés par pertinence", fs=6.8, color=M_SUB)
ax.add_patch(FancyBboxPatch((0.5, 5.0), 6.0, 0.85, boxstyle="round,pad=0.01,rounding_size=0.1", fc="white", ec=M_ACC, lw=1.1))
mtext(ax, 0.7, 5.55, "Anthelios Fluide Invisible SPF50+ — La Roche-Posay — 68,900 DT  [Voir]", fs=6.4)
ax.add_patch(FancyBboxPatch((0.5, 4.05), 6.0, 0.85, boxstyle="round,pad=0.01,rounding_size=0.1", fc="white", ec=M_LINE, lw=0.9))
mtext(ax, 0.7, 4.6, "Fusion Water SPF50 — ISDIN — 74,000 DT  [Voir]", fs=6.4)
ax.add_patch(FancyBboxPatch((0.5, 3.1), 6.0, 0.85, boxstyle="round,pad=0.01,rounding_size=0.1", fc="white", ec=M_LINE, lw=0.9))
mtext(ax, 0.7, 3.65, "Photoderm Nude Touch — Bioderma — 62,000 DT  [Voir]", fs=6.4)
ax.add_patch(FancyBboxPatch((6.9, 3.1), 2.75, 3.0, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F4F0E8", ec=M_LINE, lw=0.9))
mtext(ax, 7.15, 5.8, "Filtres", fs=7, bold=True)
mtext(ax, 7.15, 5.4, "☐ La Roche-Posay (4)", fs=6.2)
mtext(ax, 7.15, 5.05, "☐ ISDIN (2)", fs=6.2)
mtext(ax, 7.15, 4.7, "☐ Bioderma (3)", fs=6.2)
mtext(ax, 7.15, 4.3, "Prix : 40 ———● 90 DT", fs=6.2)
mtext(ax, 7.15, 3.9, "☑ En stock  ☐ En promo", fs=6.2)
mtext(ax, 7.15, 3.5, "Note min : ★★★★☆", fs=6.2)
save(f, f"{OUT}/fig78_search.png")

f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/suivi?k=9f2c…(lien privé)"); mtopnav(ax)
mtext(ax, 5, 7.0, "Commande CL-260905-K8M1", fs=10, bold=True, ha="center")
mtext(ax, 5, 6.6, "Accès invité vérifié — cette page n'est visible que via votre lien privé.", fs=6.6, color=M_ACC, ha="center")
steps = [("Reçue", True), ("Confirmée", True), ("Préparée", True), ("Expédiée", True), ("Livrée", False)]
x = 1.5
for i, (s, done) in enumerate(steps):
    ax.add_patch(Circle((x, 5.5), 0.16, fc=M_ACC if done else "white", ec=M_ACC, lw=1.2))
    if done:
        ax.text(x, 5.5, "✓", ha="center", va="center", fontsize=6, color="white", weight="bold")
    if i < 4:
        ax.plot([x + 0.16, x + 1.39], [5.5, 5.5], color=M_ACC if done else M_LINE, lw=2)
    mtext(ax, x, 5.05, s, fs=6.5, bold=done, ha="center")
    x += 1.55
mtable(ax, 1.5, 3.7, 7.0, ["Article", "Qté", "Total"],
       [["Anthelios Lait SPF50+ 250 ml", "1", "82,000"],
        ["Posthelios Après-soleil", "1", "42,000"]],
       colw=[3.6, 1.0, 1.4], rh=0.46)
mtext(ax, 5, 2.35, "Total payé à la livraison : 124,000 DT · Transporteur : TN-4471-8820", fs=6.8, bold=True, ha="center")
mtext(ax, 5, 1.9, "Le numéro seul ne suffit jamais : sans la clé de 256 bits, cette page répond « introuvable ».", fs=6, color=M_SUB, ha="center", italic=True)
save(f, f"{OUT}/fig79_guest.png")

f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/journal/choisir-sa-protection-solaire"); mtopnav(ax)
mtext(ax, 1.0, 7.0, "SOLAIRE · 6 MIN DE LECTURE", fs=6.5, bold=True, color=M_ACC)
mtext(ax, 1.0, 6.55, "Choisir sa protection solaire en Tunisie", fs=11, bold=True)
mtext(ax, 1.0, 6.1, "Par l'équipe pharmaceutique Cléopâtre · 28 août 2026", fs=6.5, color=M_SUB)
for i, t in enumerate(["Sous nos latitudes, l'indice UV dépasse 9 de mai à septembre.",
                       "Le SPF 50+ n'est pas un luxe. Pour le visage, privilégiez un",
                       "fluide invisible ; pour le corps, un lait résistant à l'eau.",
                       "La quantité compte plus que la marque : deux doigts pour",
                       "le visage, renouvelés toutes les deux heures."]):
    mtext(ax, 1.0, 5.5 - i * 0.33, t, fs=6.8)
ax.add_patch(FancyBboxPatch((6.4, 3.2), 2.6, 2.4, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F4F0E8", ec=M_LINE, lw=0.9))
mtext(ax, 6.6, 5.3, "Dans cet article", fs=6.8, bold=True)
mtext(ax, 6.6, 4.9, "• Anthelios Fluide … 68,900", fs=6.2)
mtext(ax, 6.6, 4.55, "• Fusion Water … 74,000", fs=6.2)
mtext(ax, 6.6, 4.2, "• Après-soleil … 42,000", fs=6.2)
mbtn(ax, 6.6, 3.5, 2.2, 0.45, "Voir la sélection", fs=6)
mtext(ax, 1.0, 3.0, "←  Retour au journal      Partager :  f   in   ✉", fs=6.5, color=M_ACC)
save(f, f"{OUT}/fig80_article.png")

f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/recherches"); msidebar(ax, ["Vue d'ensemble", "Support", "Recherches", "Journal"], 2)
mtext(ax, 2.5, 8.0, "Recherches des visiteurs", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "Ce que cherchent vos clients — y compris ce que vous ne vendez pas encore.", fs=6.8, color=M_SUB)
mtable(ax, 2.5, 6.35, 7.15, ["Requête", "Fois", "Résultats", "Tendance"],
       [["solaire", "214", "12", "↗ +32 %"],
        ["acide hyaluronique", "96", "8", "↗ +11 %"],
        ["shampooing sec", "41", "0 (vide)", "→ idée rayon"],
        ["rétinol", "38", "5", "↗ +8 %"]],
       colw=[2.2, 0.9, 1.3, 1.75])
mtext(ax, 2.5, 3.6, "« shampooing sec » (0 résultat, 41 fois) : opportunité d'élargir l'assortiment Cheveux.", fs=6.3, color=M_ACC)
save(f, f"{OUT}/fig81_searches.png")

f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/journal"); msidebar(ax, ["Vue d'ensemble", "Recherches", "Journal", "Boutiques"], 2)
mtext(ax, 2.5, 8.0, "Journal", fs=10, bold=True)
mbtn(ax, 8.35, 7.55, 1.3, 0.45, "+ Article", fs=6)
mtable(ax, 2.5, 6.35, 7.15, ["Titre", "Rubrique", "Lecture", "État", ""],
       [["Protection solaire en Tunisie", "Solaire", "6 min", "Publié", "Éditer"],
        ["Routine peau sensible", "Visage", "5 min", "Publié", "Éditer"],
        ["Vitamine D en hiver", "Compléments", "3 min", "Brouillon", "Éditer"]],
       colw=[2.5, 1.3, 0.9, 0.95, 0.5])
mtext(ax, 2.5, 4.0, "Le temps de lecture est calculé automatiquement (≈ 200 mots/minute).", fs=6.2, color=M_SUB, italic=True)
save(f, f"{OUT}/fig82_journal_admin.png")

# ── Fig 83 : conteneurs Docker ─────────────────────────────
f, ax = fig(6.6, 3.8)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Architecture des conteneurs Docker")
box(ax, (0.3, 4.4), 4.5, 3.4, "Conteneur « cleo-web »\n— build multi-stage —\nNext.js 16 · Node.js 22\nport 3000", fs=7.6, fc=BLUE_L, ec=BLUE, bold=True)
box(ax, (5.3, 4.4), 4.5, 3.4, "Conteneur « cleo-db »\n— image officielle —\nPostgreSQL 18 + volume\nport 5432 (interne)", fs=7.6, fc=GOLD_L, ec=GOLD)
box(ax, (0.3, 2.3), 4.5, 1.3, "Variables : DATABASE_URL · SESSION_SECRET · NEXT_PUBLIC_SITE_URL", fs=6.8, fc=SHADE, ec=MUTED)
box(ax, (5.3, 2.3), 4.5, 1.3, "Volume persistant « pgdata »\n(migration + seed au 1er démarrage)", fs=6.8, fc=SHADE, ec=MUTED)
arrow(ax, (4.8, 6.1), (5.3, 6.1), "réseau interne", fs=7)
save(f, f"{OUT}/fig83_docker.png")

# ── Fig 84 : pipeline ──────────────────────────────────────
f, ax = fig(6.6, 3.2)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Pipeline de build et de déploiement")
steps = [("git push\nmain", SHADE), ("npm ci +\ntypecheck", GOLD_L), ("next build\n+ next start", BLUE_L),
         ("docker build\n2 images", BLUE_L), ("db:push +\ndb:seed", GOLD_L), ("docker compose\nup -d", GREEN_L)]
x = 0.15
for i, (s, c) in enumerate(steps):
    box(ax, (x, 4.6), 1.5, 1.7, s, fs=6.8, fc=c, ec=MUTED if c == SHADE else INK)
    if i < 5:
        arrow(ax, (x + 1.5, 5.45), (x + 1.67, 5.45), lw=1.2)
    x += 1.67
ax.text(5, 3.6, "Build reproductible : mêmes versions Node, mêmes variables, mêmes données de démonstration.",
        ha="center", fontsize=7, color=MUTED, style="italic")
save(f, f"{OUT}/fig84_pipeline.png")

# ── Fig 85 : accueil ───────────────────────────────────────
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn"); mtopnav(ax)
ax.add_patch(Rectangle((0.15, 5.4), 9.7, 2.2, fc="#2B2620", ec="#2B2620"))
mtext(ax, 0.6, 7.0, "L'exigence pharmaceutique, l'art du soin.", fs=10, bold=True, color="#F5EFE2")
mtext(ax, 0.6, 6.55, "Dermo-cosmétique authentique, conseillée par nos pharmaciens.", fs=6.8, color="#C9A959")
ax.add_patch(FancyBboxPatch((0.6, 5.8), 1.9, 0.45, boxstyle="round,pad=0.01,rounding_size=0.08", fc="#C9A959", ec="#C9A959"))
ax.text(1.55, 6.02, "Découvrir la boutique", ha="center", va="center", fontsize=6, color="white", weight="bold")
mtext(ax, 0.6, 5.0, "Explorer par univers", fs=7.5, bold=True)
for i, u in enumerate(["Visage", "Corps", "Cheveux", "Solaire", "Bébé & Maman", "Compléments"]):
    x = 0.6 + i * 1.53
    ax.add_patch(FancyBboxPatch((x, 3.6), 1.4, 1.0, boxstyle="round,pad=0.01,rounding_size=0.1", fc="#F4F0E8", ec=M_LINE, lw=0.9))
    mtext(ax, x + 0.7, 4.1, u, fs=5.8, bold=True, ha="center")
mtext(ax, 0.6, 3.1, "Les essentiels de nos pharmaciens", fs=7.5, bold=True)
for i, (p, pr) in enumerate([("Effaclar Duo+", "62,900"), ("Anthelios Fluide", "68,900"), ("Huile Prodigieuse", "92,000"), ("Lipikar Baume", "79,900")]):
    x = 0.6 + i * 2.35
    ax.add_patch(FancyBboxPatch((x, 1.3), 2.2, 1.4, boxstyle="round,pad=0.01,rounding_size=0.1", fc="white", ec=M_LINE, lw=0.9))
    mtext(ax, x + 0.15, 2.4, p, fs=6.3, bold=True)
    mtext(ax, x + 0.15, 2.05, pr + " DT", fs=6.5, color=M_ACC, bold=True)
    mtext(ax, x + 0.15, 1.65, "★★★★★  [ Ajouter ]", fs=6.0, color=M_SUB)
save(f, f"{OUT}/fig85_home.png")

# ── Fig 86 : fiche produit ─────────────────────────────────
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/produit/…-anthelios-fluide"); mtopnav(ax)
ax.add_patch(FancyBboxPatch((0.5, 4.2), 2.9, 2.8, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F4F0E8", ec=M_LINE, lw=0.9))
mtext(ax, 1.95, 5.7, "▣  Visuel produit", fs=7, color=M_SUB, ha="center")
mtext(ax, 1.95, 5.3, "50 ml", fs=6.5, color=M_SUB, ha="center")
mtext(ax, 3.8, 6.75, "LA ROCHE-POSAY", fs=6.5, bold=True, color=M_ACC)
mtext(ax, 3.8, 6.35, "Anthelios Fluide Invisible SPF50+", fs=9, bold=True)
mtext(ax, 3.8, 5.95, "★★★★★ 4,8 · 132 avis   ·   En stock (25)   ·   ✓ Authentique", fs=6.5)
mtext(ax, 3.8, 5.5, "68,900 DT    76,000 DT barré   (-9 %)", fs=8, bold=True)
mtext(ax, 3.8, 5.05, "Protection ultra-large, fini invisible. Renouveler toutes les 2 h.", fs=6.5, color=M_SUB)
mbtn(ax, 3.8, 4.4, 2.4, 0.55, "Ajouter au panier")
mbtn(ax, 6.4, 4.4, 1.6, 0.55, "♡ Favoris", primary=False)
mtext(ax, 0.5, 3.6, "Description   |   Ingrédients   |   Conseils d'utilisation   |   Avis (132)", fs=6.8, bold=True)
mtext(ax, 0.5, 3.2, "Formulé avec une exigence pharmaceutique, sélectionné par les pharmaciens Cléopâtre…", fs=6.5, color=M_SUB)
mtext(ax, 0.5, 2.7, "Vous aimerez aussi :  [Fusion Water 74,000]  [Photoderm Nude 62,000]  [Capital Soleil 66,500]", fs=6.5, color=M_ACC)
mtext(ax, 0.5, 2.1, "Livraison 24–48 h sur le Grand Tunis · Port offert dès 99 DT · Paiement à la livraison", fs=6.3, color=M_SUB)
save(f, f"{OUT}/fig86_product.png")

print("figs4 done")
