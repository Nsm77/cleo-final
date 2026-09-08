"""Figures nouvelles : modèle consolidé release 1, modèle global, cadres AVANT (refonte)."""
import os
from mpl import *
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)

MONO = "DejaVu Sans Mono"


def cbox(ax, x, y, w, h, name, attrs, head="#2B2620"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.06",
                                fc="white", ec=INK, lw=1.0))
    ax.add_patch(FancyBboxPatch((x, y + h - 0.34), w, 0.34, boxstyle="round,pad=0.01,rounding_size=0.06",
                                fc=head, ec=head, lw=0))
    ax.add_patch(FancyBboxPatch((x, y + h - 0.34), w, 0.12, boxstyle="square,pad=0",
                                fc=head, ec="none"))
    ax.text(x + w / 2, y + h - 0.17, name, ha="center", va="center", fontsize=6.4,
            color="white", weight="bold", family=MONO)
    for i, a in enumerate(attrs):
        ax.text(x + 0.12, y + h - 0.55 - i * 0.185, a, ha="left", va="center", fontsize=5.1,
                color=INK, family=MONO)


def rel(ax, x1, y1, x2, y2, label="", dashed=False, rad=0.0):
    arrow(ax, (x1, y1), (x2, y2), label, fs=5.2, color=GOLD, ls="--" if dashed else "-",
          lw=1.0, rad=rad)


# ══ Modèle consolidé release 1 (14 classes) ═══════════════
f, ax = fig(6.6, 8.6)
ax.set_xlim(0, 10)
ax.set_ylim(1.5, 10)
ax.text(5, 9.62, "Modèle de données consolidé — release 1 (socle + commerce)",
        ha="center", va="center", fontsize=10, weight="bold", color=INK)
X = [0.12, 2.62, 5.12, 7.62]
W = 2.26
Y = [7.85, 6.08, 4.31, 2.54]
H = 1.66

cbox(ax, X[0], Y[0], W, H, "sessions", ["PK id : string(64)", "FK user_id → users", "expires_at : date", "user_agent?"], BLUE)
cbox(ax, X[1], Y[0], W, H, "users", ["PK id · UQ email", "password_hash", "first, last · phone?", "role ◆ · loyalty", "notes?"], BLUE)
cbox(ax, X[2], Y[0], W, H, "addresses", ["PK id · FK user_id", "label · full_name", "phone · line1", "city · governorat", "UQ(user) si défaut"], BLUE)
box(ax, (X[3], Y[0]), W, H, "Conventions\nPK primaire\nFK étrangère\nUQ unique · ◆ enum.\nflèches : 1 — *", fs=5.6, fc=SHADE, ec=MUTED)
cbox(ax, X[0], Y[1], W, H, "brands", ["PK id · UQ slug", "name · country?", "story? · vedette?"], GOLD)
cbox(ax, X[1], Y[1], W, H, "products", ["PK id · UQ sku", "nom · prix_mm", "stock, seuil", "statut ◆ · flags", "notes agrégées"], GOLD)
cbox(ax, X[2], Y[1], W, H, "orders", ["PK id · UQ number", "UQ access_key", "UQ idempotence?", "statut ◆ · paiement", "montants · adr JSON"], RED)
cbox(ax, X[3], Y[1], W, H, "order_events", ["PK id · FK order", "statut · message?", "acteur? · date"], RED)
cbox(ax, X[0], Y[2], W, H, "categories", ["PK id · UQ slug", "nom · univers?", "parent_id? · ordre"], GOLD)
cbox(ax, X[1], Y[2], W, H, "product_concerns", ["PK (prod, besoin)", "FK product_id", "FK concern_id"], GOLD)
cbox(ax, X[2], Y[2], W, H, "order_items", ["PK id · FK order", "FK product_id?", "snapshot nom, sku", "PU, qté, total"], RED)
cbox(ax, X[3], Y[2], W, H, "inventory_mov.", ["PK id · FK product", "type ◆ · quantité", "stock_après", "motif?"], MUTED)
cbox(ax, X[0], Y[3], W, H, "concerns", ["PK id · UQ slug", "nom · intro?"], GOLD)
cbox(ax, X[1], Y[3], W, H, "promotions", ["PK id · UQ code", "type ◆ · valeur", "min · plafond?", "quotas · validité"], GREEN)
cbox(ax, X[2], Y[3], W, H, "wishlist_items", ["PK (user, prod)", "FK user · FK prod"], MUTED)
box(ax, (X[3], Y[3]), W, H, "14 classes\n+ 6 énumérations\nDétail complet :\nAnnexe B", fs=5.8, fc="#2B2620", tc="white", ec="#2B2620")

cy = lambda r: Y[r] + H / 2
cx = lambda c: X[c] + W / 2
top = lambda r: Y[r] + H
bot = lambda r: Y[r]
rel(ax, X[1], cy(0), X[0] + W, cy(0))                 # users → sessions
rel(ax, X[1] + W, cy(0), X[2], cy(0))                 # users → addresses
rel(ax, X[0] + W, cy(1), X[1], cy(1))                 # brands → products
rel(ax, X[2] + W, cy(1), X[3], cy(1))                 # orders → events
rel(ax, cx(1), bot(1), cx(1), top(2))                 # products → pc
rel(ax, cx(2), bot(1), cx(2), top(2))                 # orders → items
rel(ax, X[0] + W, top(2), X[1], bot(1))               # categories → products (coin)
rel(ax, X[1] + W, top(2), X[2], bot(1))               # products → items (coin)
rel(ax, X[2] + W, top(2), X[3], bot(1))               # orders → inventory (coin)
rel(ax, X[0] + W, top(3), X[1], bot(2))               # concerns → pc (coin)
rel(ax, X[1] + W, bot(0), X[2], top(1))               # users → orders (coin)
ax.text(5, 1.85, "Flèches : principales clés étrangères — toutes de type « 1 — * ».",
        ha="center", fontsize=6.5, color=MUTED, style="italic")
save(f, f"{OUT}/figR1_modele.png")

# ══ Modèle global : relation client, contenu, pilotage ════
f, ax = fig(6.6, 7.6)
ax.set_xlim(0, 10)
ax.set_ylim(0.8, 10)
ax.text(5, 9.62, "Modèle de données global — relation client, contenu et pilotage",
        ha="center", va="center", fontsize=10, weight="bold", color=INK)
X = [0.12, 3.42, 6.72]
W = 3.16
Y = [7.5, 5.75, 4.0, 2.25]
H = 1.66
cbox(ax, X[0], Y[0], W, H, "reviews", ["PK id · FK produit → R1", "FK user? → R1 · auteur", "note 1-5 · titre?", "corps · statut ◆", "réponse_maison?"], GREEN)
cbox(ax, X[1], Y[0], W, H, "support_tickets", ["PK id · FK user? → R1", "email · nom", "sujet · message", "réponse? · statut ◆", "n°_commande?"], GREEN)
cbox(ax, X[2], Y[0], W, H, "articles", ["PK id · UQ slug", "titre · extrait?", "corps : texte", "rubrique? · visuel?", "lecture auto · publié?"], GREEN)
cbox(ax, X[0], Y[1], W, H, "stores", ["PK id · UQ slug", "nom · adresse, ville", "téléphone · horaires", "lien_maps? · active?"], MUTED)
cbox(ax, X[1], Y[1], W, H, "search_events", ["PK id · requête", "nb_résultats", "user? · date"], BLUE)
cbox(ax, X[2], Y[1], W, H, "analytics_events", ["PK id · nom_event", "payload JSON", "user? · date"], BLUE)
cbox(ax, X[0], Y[2], W, H, "audit_logs", ["PK id · acteur?", "action · entité", "entité_id? · détails", "date"], RED)
cbox(ax, X[1], Y[2], W, H, "loyalty_transactions", ["PK id · FK user → R1", "points ± · motif", "commande ?", "UQ(cmd) gain/perte"], RED)
cbox(ax, X[2], Y[2], W, H, "newsletter_subscribers", ["PK id · UQ email", "date_inscription"], MUTED)
cbox(ax, X[0], Y[3], W, H, "rate_limits", ["PK clé (190 car.)", "compteur · reset_at"], MUTED)
box(ax, (X[1], Y[3]), W, H, "Release 1\n14 classes\n(figure précédente)\nliens marqués « → R1 »", fs=5.6, fc=SHADE, ec=MUTED, ls="--")
box(ax, (X[2], Y[3]), W, H, "Total : 24 tables\n+ 10 énumérations\ncontraintes + index\ntransactions ACID", fs=5.6, fc="#2B2620", tc="white", ec="#2B2620")
ax.text(5, 1.35, "Tables autonomes : aucune clé étrangère interne — les liens « → R1 » pointent vers la release 1.",
        ha="center", fontsize=6.5, color=MUTED, style="italic")
save(f, f"{OUT}/figGX_modele.png")

# ══ Cadres AVANT (à remplir par l'étudiant) ═══════════════
def avant_frame(path, page, conseil):
    f, ax = fig(6.6, 3.6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.add_patch(FancyBboxPatch((0.2, 0.5), 9.6, 8.9, boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="#FBF8F1", ec=GOLD, lw=1.6, ls=(0, (6, 3))))
    ax.add_patch(FancyBboxPatch((3.6, 8.0), 2.8, 0.9, boxstyle="round,pad=0.02,rounding_size=0.3",
                                fc="#2B2620", ec="#2B2620", lw=0))
    ax.text(5, 8.45, "A V A N T", ha="center", va="center", fontsize=11, color="#C9A959", weight="bold")
    ax.text(5, 7.1, f"Ancien site — {page}", ha="center", va="center", fontsize=10, color=INK, weight="bold")
    ax.text(5, 6.1, "Insérez ici votre capture d'écran de l'ancien site (avant refonte).", ha="center",
            va="center", fontsize=8, color=MUTED)
    ax.text(5, 5.3, conseil, ha="center", va="center", fontsize=7.5, color=MUTED, style="italic")
    ax.text(5, 4.2, "Marche à suivre : remplacez ce fichier image par votre capture (même nom),", ha="center",
            va="center", fontsize=7, color=MUTED)
    ax.text(5, 3.7, "puis régénérez le rapport :  python build.py", ha="center", va="center", fontsize=7,
            color=MUTED, family=MONO)
    ax.text(5, 2.6, "▣  Emplacement réservé — 150 mm de large", ha="center", va="center", fontsize=8, color=GOLD)
    ax.text(5, 1.5, os.path.basename(path), ha="center", va="center", fontsize=7, color=MUTED, family=MONO)
    save(f, path)

C = "Conseil : capture à 1600 px de large, format PNG."
avant_frame(f"{OUT}/avant_accueil.png", "page d'accueil", C)
avant_frame(f"{OUT}/avant_boutique.png", "page boutique / catalogue", C)
avant_frame(f"{OUT}/avant_produit.png", "fiche produit", C)
avant_frame(f"{OUT}/avant_commande.png", "panier / commande", C)
avant_frame(f"{OUT}/avant_suivi.png", "suivi de commande", C)
avant_frame(f"{OUT}/avant_admin.png", "administration", C)
print("figs5 done")
