"""Figures 45-62 : sprint 2 (catalogue, promotions, commandes)."""
import os
from mpl import *
from figs1 import uc_diagram
from figs2 import (seq_diagram, class_box, browser, mtext, mbtn, mfield, mtable,
                   msidebar, mtopnav, M_SUB, M_TXT, M_ACC, M_LINE, M_BTN)
from matplotlib.patches import FancyBboxPatch, Circle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)

# ── Figs 45-48 : UC sprint 2 ───────────────────────────────
uc_diagram(f"{OUT}/fig45_uc_products.png", "Diagramme du cas d'utilisation « Gérer les produits »",
    ["Administrateur"], ["Client"],
    ["Consulter le catalogue", "Ajouter un produit", "Modifier un produit",
     "Archiver un produit", "Ajuster le stock"],
    [("Administrateur", "Ajouter un produit"), ("Administrateur", "Modifier un produit"),
     ("Administrateur", "Archiver un produit"), ("Administrateur", "Ajuster le stock"),
     ("Administrateur", "Consulter le catalogue"), ("Client", "Consulter le catalogue")])
uc_diagram(f"{OUT}/fig46_uc_promos.png", "Diagramme du cas d'utilisation « Gérer les promotions »",
    ["Administrateur"], ["Client"],
    ["Créer un code promo", "Désactiver un code", "Appliquer un code", "Voir les offres"],
    [("Administrateur", "Créer un code promo"), ("Administrateur", "Désactiver un code"),
     ("Client", "Appliquer un code"), ("Client", "Voir les offres")])
uc_diagram(f"{OUT}/fig47_uc_orders.png", "Diagramme du cas d'utilisation « Gérer les commandes »",
    ["Client"], ["Admin / Support"],
    ["Passer commande", "Annuler commande", "Demander un retour",
     "Changer le statut", "Ajouter une note interne"],
    [("Client", "Passer commande"), ("Client", "Annuler commande"), ("Client", "Demander un retour"),
     ("Admin / Support", "Changer le statut"), ("Admin / Support", "Ajouter une note interne")])
uc_diagram(f"{OUT}/fig48_uc_history.png", "Diagramme du cas d'utilisation « Consulter l'historique des commandes »",
    ["Client"], ["Admin / Support"],
    ["Voir mes commandes", "Voir le détail + timeline", "Suivre un colis invité"],
    [("Client", "Voir mes commandes"), ("Client", "Voir le détail + timeline"),
     ("Client", "Suivre un colis invité"), ("Admin / Support", "Voir le détail + timeline")])

# ── Fig 49 : machine à états commande ─────────────────────
f, ax = fig(6.6, 3.4)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Machine à états du cycle de vie d'une commande")
states = ["En attente", "Confirmée", "En préparation", "Expédiée", "Livrée"]
x = 0.25
for i, s in enumerate(states):
    box(ax, (x, 5.6), 1.7, 1.2, s, fs=7.2, fc=BLUE_L if i < 4 else GREEN_L, ec=BLUE if i < 4 else GREEN, bold=(i == 0))
    if i < 4:
        arrow(ax, (x + 1.7, 6.2), (x + 1.95, 6.2), lw=1.2)
    x += 1.95
box(ax, (0.25, 3.3), 1.7, 1.1, "Annulée", fs=7.2, fc=RED_L, ec=RED)
box(ax, (2.2, 3.3), 1.7, 1.1, "Retournée", fs=7.2, fc=RED_L, ec=RED)
arrow(ax, (1.1, 5.6), (1.1, 4.4), "annuler", fs=6.8, color=RED)
arrow(ax, (8.35, 5.6), (8.35, 4.4), "", fs=6.8, color=RED)
arrow(ax, (8.35, 4.4), (3.05, 4.4), "retour", fs=6.8, color=RED)
ax.text(5, 2.5, "Transitions autorisées uniquement (ALLOWED_TRANSITIONS) — toute autre transition est rejetée.",
        ha="center", fontsize=7, color=MUTED, style="italic")
save(f, f"{OUT}/fig49_statemachine.png")

# ── Fig 50 : classes sprint 2 ──────────────────────────────
f, ax = fig(6.6, 4.6)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Diagramme de classes — sprint 2 (commerce)")
class_box(ax, 0.2, 5.6, 3.1, 3.0, "Product",
    ["+ sku, slug, name", "+ priceMillimes : int", "+ compareAt?", "+ stock, threshold", "+ status : enum", "+ ratingAvg/Count"],
    ["+ isLowStock()"], BLUE_L)
class_box(ax, 3.55, 5.6, 3.1, 3.0, "Order",
    ["+ number, accessKey", "+ idempotencyKey", "+ status : enum", "+ payment / shipping", "+ subtotal/discount/", "+ shipping/total"],
    ["+ canCancel()"], GOLD_L)
class_box(ax, 6.9, 5.6, 2.9, 3.0, "OrderItem",
    ["+ orderId FK", "+ productId FK?", "+ snapshot : nom, sku", "+ unitPrice, qty", "+ lineTotal"], None, GOLD_L)
class_box(ax, 0.2, 1.9, 3.1, 2.9, "Promotion",
    ["+ code, label", "+ type : enum", "+ value, minSubtotal", "+ maxDiscount?", "+ usageLimit/Count", "+ perUserLimit"],
    ["+ evaluate()"], GREEN_L)
class_box(ax, 3.55, 1.9, 3.1, 2.9, "OrderEvent",
    ["+ orderId FK", "+ status, message", "+ actorId?, date"], None, SHADE)
class_box(ax, 6.9, 1.9, 2.9, 2.9, "InventoryMovement",
    ["+ productId FK", "+ type : enum", "+ quantity, stockAfter", "+ reason, orderId?"], None, SHADE)
arrow(ax, (6.65, 7.1), (6.9, 7.1), "1 — *", fs=7)
arrow(ax, (5.1, 5.6), (5.1, 4.85), "1 — *", fs=7)
arrow(ax, (1.75, 5.6), (1.75, 4.85), "1 — *", fs=7)
save(f, f"{OUT}/fig50_classes_s2.png")

# ── Figs 51-53 : séquences sprint 2 ────────────────────────
seq_diagram(f"{OUT}/fig51_seq_addproduct.png", "Diagramme de séquence « Ajouter un produit »",
    ["Admin", "Fiche produit", "saveProductAction", "PostgreSQL"],
    [(0, 1, "remplir fiche + prix DT", False), (1, 2, "saveProductAction(form)", False),
     (2, 2, "requireAdmin + Zod (DT→millimes)", False), (2, 3, "BEGIN + INSERT product", False),
     (2, 3, "INSERT stock initial + concerns", False), (3, 2, "COMMIT", True),
     (2, 1, "ok + revalidation /boutique", True)])
seq_diagram(f"{OUT}/fig52_seq_checkout.png", "Diagramme de séquence « Passer une commande »",
    ["Client", "Tunnel /commande", "placeOrderAction", "PostgreSQL"],
    [(0, 1, "valider le récapitulatif", False), (1, 2, "placeOrderAction(données)", False),
     (2, 2, "origine + quota + Zod", False), (2, 3, "verrou idempotence (advisory)", False),
     (2, 3, "SELECT … FOR UPDATE (produits)", False), (2, 3, "réserver le code promo (verrou)", False),
     (2, 3, "INSERT order + items + mouvements", False), (3, 2, "COMMIT", True),
     (2, 1, "numéro + clé d'accès", True)])
seq_diagram(f"{OUT}/fig53_seq_status.png", "Diagramme de séquence « Changer le statut d'une commande »",
    ["Staff", "Détail commande", "updateOrderStatus", "PostgreSQL"],
    [(0, 1, "choisir le nouveau statut", False), (1, 2, "updateOrderStatusAction()", False),
     (2, 2, "requireStaff + transition autorisée ?", False), (2, 3, "lockOrder (FOR UPDATE)", False),
     (2, 3, "UPDATE conditionnel + event", False), (2, 3, "fidélité / restock selon cas", False),
     (3, 2, "COMMIT", True), (2, 1, "ok : statut mis à jour", True)])

# ── Figs 54-62 : interfaces sprint 2 ───────────────────────
# 54 ajout produit
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/produits/nouveau"); msidebar(ax, ["Vue d'ensemble", "Produits", "Stock", "Promotions"], 1)
mtext(ax, 2.5, 8.0, "Nouveau produit", fs=10, bold=True)
mfield(ax, 2.5, 6.9, 4.6, 0.48, "Nom", "Effaclar Gel Moussant Purifiant")
mfield(ax, 7.3, 6.9, 2.2, 0.48, "SKU", "CL-0001")
mfield(ax, 2.5, 5.9, 2.25, 0.48, "Marque", "La Roche-Posay ▾")
mfield(ax, 4.95, 5.9, 2.25, 0.48, "Univers", "Visage ▾")
mfield(ax, 7.4, 5.9, 2.1, 0.48, "Prix (DT)", "42,900")
mfield(ax, 2.5, 4.9, 2.25, 0.48, "Ancien prix", "47,500")
mfield(ax, 4.95, 4.9, 2.25, 0.48, "Stock initial", "40")
mfield(ax, 7.4, 4.9, 2.1, 0.48, "Statut", "Actif ▾")
mtext(ax, 2.5, 4.35, "☑ Vedette    ☑ Nouveauté    Besoins : ☑ Imperfections  ☑ Peau sensible", fs=6.3)
mbtn(ax, 2.5, 3.55, 1.8, 0.5, "Enregistrer")
mbtn(ax, 4.5, 3.55, 1.5, 0.5, "Annuler", primary=False)
save(f, f"{OUT}/fig54_product_add.png")

# 55 liste produits
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/produits"); msidebar(ax, ["Vue d'ensemble", "Produits", "Stock", "Promotions"], 1)
mtext(ax, 2.5, 8.0, "Produits", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "81 références · filtrer par univers, marque, statut", fs=6.8, color=M_SUB)
mbtn(ax, 8.35, 7.55, 1.3, 0.45, "+ Produit", fs=6)
mtable(ax, 2.5, 6.3, 7.15, ["Produit", "Prix", "Stock", "Statut", ""],
       [["Effaclar Gel Moussant", "42,900", "40", "Actif", "Éditer"],
        ["Toleriane Sensitive", "59,900", "3 ⚠", "Actif", "Éditer"],
        ["Huile Prodigieuse", "92,000", "0 (rupture)", "Actif", "Éditer"],
        ["Anthelios Fluide SPF50+", "68,900", "25", "Actif", "Éditer"]],
       colw=[2.4, 1.1, 1.0, 1.0, 0.65])
mtext(ax, 2.5, 3.3, "⚠ stock bas (≤ seuil) · alerte rupture — réassort depuis l'écran Stock & inventaire.", fs=6.2, color=M_SUB, italic=True)
save(f, f"{OUT}/fig55_products_list.png")

# 56 ajout promo
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/promotions/nouveau"); msidebar(ax, ["Vue d'ensemble", "Produits", "Stock", "Promotions"], 3)
mtext(ax, 2.5, 8.0, "Nouvelle promotion", fs=10, bold=True)
mfield(ax, 2.5, 6.9, 2.2, 0.48, "Code", "SOLAIRE15")
mfield(ax, 4.9, 6.9, 4.6, 0.48, "Libellé", "-15 % sur l'univers Solaire")
mfield(ax, 2.5, 5.9, 2.2, 0.48, "Type", "Pourcentage ▾")
mfield(ax, 4.9, 5.9, 2.2, 0.48, "Valeur", "15")
mfield(ax, 7.3, 5.9, 2.2, 0.48, "Min. d'achat (DT)", "0")
mfield(ax, 2.5, 4.9, 2.2, 0.48, "Plafond remise", "—")
mfield(ax, 4.9, 4.9, 2.2, 0.48, "Limite / client", "1")
mfield(ax, 7.3, 4.9, 2.2, 0.48, "Expire le", "30/09/2026")
mbtn(ax, 2.5, 3.9, 1.8, 0.5, "Enregistrer")
mbtn(ax, 4.5, 3.9, 1.5, 0.5, "Annuler", primary=False)
save(f, f"{OUT}/fig56_promo_add.png")

# 57 liste promos
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/promotions"); msidebar(ax, ["Vue d'ensemble", "Produits", "Stock", "Promotions"], 3)
mtext(ax, 2.5, 8.0, "Promotions", fs=10, bold=True)
mbtn(ax, 8.35, 7.55, 1.3, 0.45, "+ Promo", fs=6)
mtable(ax, 2.5, 6.4, 7.15, ["Code", "Offre", "Utilisations", "Actif", ""],
       [["BIENVENUE10", "-10 % dès 50 DT", "87 / ∞", "●", "Éditer"],
        ["SOLAIRE15", "-15 % Solaire", "203 / ∞", "●", "Éditer"],
        ["LIVRAISON", "Port offert dès 40 DT", "154 / ∞", "●", "Éditer"],
        ["CLEO20", "-20 DT dès 150 DT", "200 / 200", "○", "Éditer"]],
       colw=[1.5, 2.2, 1.5, 0.7, 0.7])
mtext(ax, 2.5, 3.5, "Consommation atomique : le compteur ne dépasse jamais sa limite, même en cas d'achats simultanés.", fs=6.2, color=M_SUB, italic=True)
save(f, f"{OUT}/fig57_promos_list.png")

# 58 tunnel étapes 1-2
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/commande"); mtopnav(ax)
mtext(ax, 0.5, 7.1, "① Informations   ② Livraison   ③ Paiement   ④ Récapitulatif", fs=6.8, color=M_ACC, bold=True)
mtext(ax, 0.5, 6.6, "Vos informations", fs=9, bold=True)
mfield(ax, 0.5, 5.6, 3.2, 0.48, "E-mail", "ines.mansour@mail.tn")
mfield(ax, 3.9, 5.6, 2.6, 0.48, "Téléphone", "22 345 678")
mfield(ax, 0.5, 4.6, 6.0, 0.48, "Adresse", "12 rue des Jasmins")
mfield(ax, 0.5, 3.6, 1.9, 0.48, "Ville", "Ezzahra")
mfield(ax, 2.6, 3.6, 1.9, 0.48, "Gouvernorat", "Ben Arous ▾")
mfield(ax, 4.6, 3.6, 1.9, 0.48, "Code postal", "2034")
ax.add_patch(FancyBboxPatch((6.9, 3.0), 2.75, 3.6, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F4F0E8", ec=M_LINE, lw=0.9))
mtext(ax, 7.15, 6.3, "Récapitulatif", fs=7, bold=True)
mtext(ax, 7.15, 5.9, "Effaclar Duo+ × 1 …… 62,900", fs=6.2)
mtext(ax, 7.15, 5.55, "Cicaplast Mains × 2 … 45,800", fs=6.2)
mtext(ax, 7.15, 5.2, "Livraison standard …… 7,000", fs=6.2)
mtext(ax, 7.15, 4.8, "Code : [SOLAIRE15] [OK]", fs=6.2, color=M_ACC)
mtext(ax, 7.15, 4.3, "Total : 115,700 DT", fs=7, bold=True)
mtext(ax, 7.15, 3.9, "Plus que 33,400 DT avant le port offert.", fs=5.8, color=M_SUB)
mtext(ax, 7.15, 3.5, "Livraison estimée : 24–48 h (Ben Arous).", fs=5.8, color=M_SUB)
mbtn(ax, 0.5, 2.5, 2.2, 0.55, "Continuer →")
save(f, f"{OUT}/fig58_checkout12.png")

# 59 tunnel étapes 3-4
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/commande"); mtopnav(ax)
mtext(ax, 0.5, 7.1, "① Informations   ② Livraison   ③ Paiement   ④ Récapitulatif", fs=6.8, color=M_ACC, bold=True)
mtext(ax, 0.5, 6.6, "Paiement", fs=9, bold=True)
for i, (t, sub, on) in enumerate([("Paiement à la livraison", "Espèces ou TPE à la réception", True),
                                  ("Virement bancaire", "RIB envoyé après validation", False),
                                  ("Carte cadeau", "Code vérifié par téléphone", False)]):
    y = 5.9 - i * 0.85
    ax.add_patch(FancyBboxPatch((0.5, y - 0.32), 6.0, 0.68, boxstyle="round,pad=0.01,rounding_size=0.1",
                                fc="white", ec=M_ACC if on else M_LINE, lw=1.2 if on else 0.9))
    mtext(ax, 0.8, y + 0.08, ("◉ " if on else "○ ") + t, fs=6.8, bold=on)
    mtext(ax, 1.35, y - 0.18, sub, fs=6.0, color=M_SUB)
mtext(ax, 0.5, 2.55, "☐ Emballage cadeau (+5,000 DT)    ☐ Créer mon compte (mot de passe : …………)", fs=6.4)
mbtn(ax, 0.5, 1.75, 2.6, 0.55, "Confirmer la commande")
mtext(ax, 3.35, 2.02, "Transaction sécurisée · anti double-clic", fs=6.0, color=M_SUB, italic=True)
ax.add_patch(FancyBboxPatch((6.9, 1.7), 2.75, 3.6, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F4F0E8", ec=M_LINE, lw=0.9))
mtext(ax, 7.15, 5.0, "Total à payer", fs=7, bold=True)
mtext(ax, 7.15, 4.55, "115,700 DT", fs=10, bold=True, color=M_ACC)
mtext(ax, 7.15, 4.0, "dont TVA incluse · 2 articles", fs=6.0, color=M_SUB)
mtext(ax, 7.15, 3.4, "+11 points fidélité à la livraison.", fs=6.0, color=M_SUB)
mtext(ax, 7.15, 2.6, "En confirmant, vous acceptez nos CGV.", fs=5.8, color=M_SUB)
save(f, f"{OUT}/fig59_checkout34.png")

# 60 liste commandes admin
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/commandes"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Produits", "Stock"], 1)
mtext(ax, 2.5, 8.0, "Commandes", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "Filtres : [Toutes ▾] [Recherche n° / client…]   [Exporter CSV]", fs=6.5, color=M_ACC)
mtable(ax, 2.5, 6.5, 7.15, ["N°", "Cliente", "Total", "Statut", ""],
       [["CL-260907-X7K2", "Ines M.", "115,700", "En attente", "Ouvrir"],
        ["CL-260906-P9D4", "Amira B.", "52,900", "Confirmée", "Ouvrir"],
        ["CL-260905-K8M1", "Salma R.", "124,000", "Expédiée", "Ouvrir"],
        ["CL-260904-T2V7", "Rim H.", "38,500", "Livrée", "Ouvrir"],
        ["CL-260903-B6N3", "Yasmine K.", "74,200", "Annulée", "Ouvrir"]],
       colw=[1.9, 1.2, 1.1, 1.25, 0.7])
save(f, f"{OUT}/fig60_orders_list.png")

# 61 détail commande admin
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/commandes/42"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Produits"], 1)
mtext(ax, 2.5, 8.0, "CL-260907-X7K2  ·  En attente", fs=9.5, bold=True)
mtext(ax, 2.5, 7.6, "Ines Mansour · 22 345 678 · Paiement à la livraison · 12 rue des Jasmins, Ezzahra", fs=6.5, color=M_SUB)
mtable(ax, 2.5, 6.35, 4.6, ["Article", "Qté", "Total"],
       [["Effaclar Duo+ 40 ml", "1", "62,900"],
        ["Cicaplast Mains", "2", "45,800"],
        ["Livraison standard", "—", "7,000"]],
       colw=[2.3, 0.7, 1.0], rh=0.46)
mtext(ax, 2.5, 4.35, "Total : 115,700 DT   ·   Code : —", fs=7, bold=True)
mtext(ax, 7.4, 6.9, "Faire avancer :", fs=6.5, bold=True)
mbtn(ax, 7.4, 6.3, 2.1, 0.45, "Confirmer ✓", fs=6.2)
ax.add_patch(FancyBboxPatch((7.4, 5.7), 2.1, 0.45, boxstyle="round,pad=0.01,rounding_size=0.08", fc="white", ec="#A34A3E", lw=0.9))
ax.text(8.45, 5.92, "Annuler ✕", ha="center", va="center", fontsize=6.2, color="#A34A3E", weight="bold")
mtext(ax, 7.4, 5.15, "Timeline :", fs=6.5, bold=True)
mtext(ax, 7.4, 4.8, "● Commande reçue — 09:12", fs=6.0)
mtext(ax, 7.4, 4.45, "○ Confirmation — en attente", fs=6.0, color=M_SUB)
mfield(ax, 2.5, 3.35, 4.6, 0.5, "Note interne", "Appeler avant 14 h.")
mfield(ax, 7.4, 3.35, 2.1, 0.5, "N° suivi", "TN-4471…")
save(f, f"{OUT}/fig61_order_detail.png")

# 62 suivi client
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/suivi"); mtopnav(ax)
mtext(ax, 5, 7.0, "Suivre ma commande", fs=10, bold=True, ha="center")
mfield(ax, 2.6, 5.9, 2.6, 0.5, "N° de commande", "CL-260905-K8M1")
mfield(ax, 5.4, 5.9, 2.6, 0.5, "E-mail", "salma.r@mail.tn")
mbtn(ax, 8.2, 5.9, 1.3, 0.5, "Suivre", fs=6.5)
# timeline
steps = [("Reçue", "04/09 · 10:02", True), ("Confirmée", "04/09 · 11:40", True),
         ("Préparée", "05/09 · 09:15", True), ("Expédiée", "05/09 · 16:20", True), ("Livrée", "en cours…", False)]
x = 1.1
for i, (s, d, done) in enumerate(steps):
    ax.add_patch(Circle((x, 4.6), 0.16, fc=M_ACC if done else "white", ec=M_ACC, lw=1.2))
    if done:
        ax.text(x, 4.6, "✓", ha="center", va="center", fontsize=6, color="white", weight="bold")
    if i < 4:
        ax.plot([x + 0.16, x + 1.55], [4.6, 4.6], color=M_ACC if done else M_LINE, lw=2)
    mtext(ax, x, 4.15, s, fs=6.5, bold=done, ha="center")
    mtext(ax, x, 3.8, d, fs=5.8, color=M_SUB, ha="center")
    x += 1.71
ax.add_patch(FancyBboxPatch((1.1, 2.5), 7.8, 0.8, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#F4F0E8", ec=M_LINE, lw=0.9))
mtext(ax, 5, 3.05, "Votre colis est entre les mains du transporteur — livraison estimée demain avant 18 h.", fs=6.6, ha="center")
mtext(ax, 5, 1.9, "Lien privé de suivi envoyé par e-mail : seul le détenteur de la clé d'accès voit cette page.", fs=6, color=M_SUB, ha="center", italic=True)
save(f, f"{OUT}/fig62_suivi.png")

print("figs3 done")
