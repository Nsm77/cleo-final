"""Figures 23-44 : sprint 1 (socle, UC, classes, séquences, interfaces). + helpers séquence/classes/maquettes."""
import os
from mpl import *
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)
from figs1 import uc_diagram  # noqa: E402

# ══ helpers diagrammes de séquence ════════════════════════
def seq_diagram(path, title_t, actors, messages, notes=None, w_in=6.6, h_in=4.0):
    f, ax = fig(w_in, h_in)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    title(ax, title_t)
    n = len(actors)
    xs = [1.0 + i * (8.0 / (n - 1)) for i in range(n)] if n > 1 else [5.0]
    top, bottom = 8.6, 1.2
    for x, a in zip(xs, actors):
        box(ax, (x - 0.85, top), 1.7, 0.62, a, fs=7.4, fc=BLUE_L, ec=BLUE, bold=True)
        ax.plot([x, x], [top, bottom], color=MUTED, lw=0.9, ls="--")
    m = len(messages)
    ys = [top - 0.9 - i * ((top - 1.4 - bottom) / max(1, m)) for i in range(m)]
    for (frm, to, label, dashed), y in zip(messages, ys):
        x1, x2 = xs[frm], xs[to]
        if frm == to:
            ax.plot([x1, x1 + 0.6, x1 + 0.6, x1], [y, y, y - 0.35, y - 0.35], color=INK, lw=1.0)
            ax.text(x1 + 0.3, y + 0.1, label, fontsize=7, color=INK, va="bottom", ha="center",
                    bbox=dict(fc=PAPER, ec="none", pad=1.2))
        else:
            arrow(ax, (x1, y), (x2, y), label, fs=7, ls="--" if dashed else "-", lw=1.0)
    if notes:
        for i, nt in enumerate(notes):
            ax.text(5, 0.95 - i * 0.3, nt, ha="center", fontsize=6.8, color=MUTED, style="italic")
    save(f, path)

# ══ helpers diagrammes de classes ═════════════════════════
def class_box(ax, x, y, w, h, name, attrs, methods=None, fc=PAPER):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.01", fc=fc, ec=INK, lw=1.1))
    ax.plot([x, x + w], [y + h - 0.5, y + h - 0.5], color=INK, lw=0.9)
    ax.text(x + w / 2, y + h - 0.25, name, ha="center", va="center", fontsize=8, weight="bold")
    for i, a in enumerate(attrs):
        ax.text(x + 0.15, y + h - 0.75 - i * 0.3, a, ha="left", va="center", fontsize=6.9, family="DejaVu Sans Mono")
    if methods:
        my = y + h - 0.75 - len(attrs) * 0.3 - 0.1
        ax.plot([x, x + w], [my, my], color=INK, lw=0.9)
        for i, md in enumerate(methods):
            ax.text(x + 0.15, my - 0.25 - i * 0.3, md, ha="left", va="center", fontsize=6.9, family="DejaVu Sans Mono")

# ══ helpers maquettes d'interfaces ════════════════════════
M_BG, M_CARD, M_LINE, M_TXT, M_SUB, M_ACC, M_BTN = "#FFFFFF", "#F4F0E8", "#D8CFBE", "#2B2620", "#8d8474", "#8C6924", "#2B2620"

def browser(ax, url="cleopatre.tn"):
    ax.add_patch(FancyBboxPatch((0.15, 0.35), 9.7, 9.05, boxstyle="round,pad=0.02,rounding_size=0.18",
                                fc="white", ec=M_LINE, lw=1.2))
    ax.add_patch(FancyBboxPatch((0.15, 8.55), 9.7, 0.85, boxstyle="round,pad=0.02,rounding_size=0.18",
                                fc="#EFE9DC", ec=M_LINE, lw=1.0))
    for i, c in enumerate(["#D96A5F", "#E8B44C", "#7FB069"]):
        ax.add_patch(Circle((0.55 + i * 0.32, 8.98), 0.09, fc=c, ec=c))
    ax.add_patch(FancyBboxPatch((1.7, 8.78), 6.6, 0.42, boxstyle="round,pad=0.01,rounding_size=0.2",
                                fc="white", ec=M_LINE, lw=0.8))
    ax.text(4.95, 8.99, url, ha="center", va="center", fontsize=6.5, color=M_SUB, family="DejaVu Sans Mono")

def mtext(ax, x, y, s, fs=7, bold=False, color=M_TXT, ha="left", va="center", italic=False):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color,
            weight="bold" if bold else "normal", style="italic" if italic else "normal")

def mbtn(ax, x, y, w, h, s, primary=True, fs=6.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.08",
                                fc=M_BTN if primary else "white", ec=M_BTN, lw=0.9))
    ax.text(x + w / 2, y + h / 2, s, ha="center", va="center", fontsize=fs,
            color="white" if primary else M_BTN, weight="bold")

def mfield(ax, x, y, w, h, label, value="", fs=6.3):
    mtext(ax, x, y + h + 0.22, label, fs=fs, color=M_SUB)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.08",
                                fc="white", ec=M_LINE, lw=0.9))
    if value:
        ax.text(x + 0.12, y + h / 2, value, ha="left", va="center", fontsize=fs, color=M_TXT,
                family="DejaVu Sans Mono" if "@" in value or "•" in value else "DejaVu Sans")

def mtable(ax, x, y, w, headers, rows, fs=6.3, rh=0.52, colw=None):
    n = len(headers)
    colw = colw or [w / n] * n
    # header
    cx = x
    for i, h in enumerate(headers):
        ax.add_patch(Rectangle((cx, y), colw[i], rh, fc=M_BTN, ec=M_BTN))
        ax.text(cx + colw[i] / 2, y + rh / 2, h, ha="center", va="center", fontsize=fs, color="white", weight="bold")
        cx += colw[i]
    yy = y - rh
    for r, row in enumerate(rows):
        cx = x
        bg = "#FAF7F0" if r % 2 else "white"
        for i, c in enumerate(row):
            ax.add_patch(Rectangle((cx, yy), colw[i], rh, fc=bg, ec=M_LINE, lw=0.7))
            ax.text(cx + 0.1, yy + rh / 2, str(c), ha="left", va="center", fontsize=fs, color=M_TXT)
            cx += colw[i]
        yy -= rh
    return yy

def msidebar(ax, items, active=0):
    ax.add_patch(Rectangle((0.15, 0.35), 2.0, 8.2, fc="#2B2620", ec="#2B2620"))
    mtext(ax, 0.45, 8.15, "CLÉOPÂTRE", fs=6.5, bold=True, color="#C9A959")
    mtext(ax, 0.45, 7.8, "Administration", fs=5.8, color="#8d8474")
    y = 7.25
    for i, it in enumerate(items):
        if i == active:
            ax.add_patch(Rectangle((0.15, y - 0.2), 2.0, 0.44, fc="#C9A959", ec="#C9A959"))
            mtext(ax, 0.45, y + 0.02, it, fs=6.3, bold=True, color="white")
        else:
            mtext(ax, 0.45, y + 0.02, it, fs=6.3, color="#D8CFBE")
        y -= 0.52

def mtopnav(ax, items=("Boutique", "Univers", "Marques", "Offres", "Journal")):
    ax.add_patch(Rectangle((0.15, 7.6), 9.7, 0.95, fc="white", ec=M_LINE, lw=0.9))
    mtext(ax, 0.5, 8.08, "CLÉOPÂTRE", fs=7.5, bold=True)
    x = 2.6
    for it in items:
        mtext(ax, x, 8.08, it, fs=6.3, color=M_SUB)
        x += 1.05
    mtext(ax, 9.35, 8.08, "Recherche · Compte · Panier (2)", fs=6.0, ha="right", color=M_SUB)

def mkpi(ax, x, y, w, label, value, sub):
    ax.add_patch(FancyBboxPatch((x, y), w, 1.05, boxstyle="round,pad=0.01,rounding_size=0.1",
                                fc="white", ec=M_LINE, lw=0.9))
    mtext(ax, x + 0.15, y + 0.82, label, fs=5.6, color=M_SUB)
    mtext(ax, x + 0.15, y + 0.5, value, fs=8.5, bold=True)
    mtext(ax, x + 0.15, y + 0.2, sub, fs=5.6, color=M_ACC)

# ── Fig 23 : chaîne scrypt & sessions ─────────────────────
f, ax = fig(6.6, 3.2)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Chaîne de hachage scrypt et gestion des sessions")
box(ax, (0.2, 5.2), 1.7, 1.5, "Mot de passe\n+ sel aléatoire", fs=7, fc=SHADE, ec=MUTED)
box(ax, (2.3, 5.2), 1.7, 1.5, "scrypt\n(N=2^?, 64 o)", fs=7, fc=GOLD_L, ec=GOLD, bold=True)
box(ax, (4.4, 5.2), 1.7, 1.5, "Empreinte\nstockée (BD)", fs=7, fc=SHADE, ec=MUTED)
box(ax, (6.5, 5.2), 1.7, 1.5, "Session 256 bits\ntable sessions", fs=7, fc=BLUE_L, ec=BLUE)
box(ax, (8.2, 5.2), 1.6, 1.5, "Cookie\nhttpOnly", fs=7, fc=GREEN_L, ec=GREEN)
for a, b in [(1.9, 2.3), (4.0, 4.4), (6.1, 6.5), (8.2 - 0.0, 8.2)]:
    arrow(ax, (a, 5.95), (b, 5.95), lw=1.2)
box(ax, (2.3, 3.0), 5.9, 1.2, "Vérification en temps constant (timingSafeEqual) + purge automatique des sessions expirées", fs=7, fc=PAPER, ec=INK, ls="--")
arrow(ax, (5.25, 5.2), (5.25, 4.2), style="-", color=MUTED)
save(f, f"{OUT}/fig23_scrypt.png")

# ── Fig 24 : rôles et gardes ───────────────────────────────
f, ax = fig(6.6, 3.6)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Hiérarchie des rôles et gardes d'accès")
box(ax, (0.3, 5.4), 2.9, 1.9, "Visiteur\n(anonyme)", fs=7.8, fc=SHADE, ec=MUTED)
box(ax, (3.6, 5.4), 2.9, 1.9, "Client\nconnecté", fs=7.8, fc=BLUE_L, ec=BLUE)
box(ax, (6.9, 5.4), 2.9, 1.9, "Équipe\nsupport · admin", fs=7.8, fc=GOLD_L, ec=GOLD, bold=True)
box(ax, (0.3, 3.3), 2.9, 1.3, "catalogue · panier\ncommande invité", fs=7, fc=PAPER, ec=MUTED, ls="--")
box(ax, (3.6, 3.3), 2.9, 1.3, "compte · favoris\n+ requireUser()", fs=7, fc=PAPER, ec=BLUE, ls="--")
box(ax, (6.9, 3.3), 2.9, 1.3, "/admin · require-\nStaff() / Admin()", fs=7, fc=PAPER, ec=GOLD, ls="--")
arrow(ax, (3.2, 6.35), (3.6, 6.35), "connexion", fs=7)
arrow(ax, (6.5, 6.35), (6.9, 6.35), "rôle staff", fs=7)
for x in (1.75, 5.05, 8.35):
    arrow(ax, (x, 5.4), (x, 4.6), style="-", color=MUTED)
save(f, f"{OUT}/fig24_roles.png")

# ── Figs 25-28 : UC sprint 1 ───────────────────────────────
uc_diagram(f"{OUT}/fig25_uc_auth.png", "Diagramme du cas d'utilisation « S'authentifier »",
    ["Visiteur"], [],
    ["S'inscrire", "Se connecter", "Se déconnecter", "Mot de passe oublié"],
    [("Visiteur", "S'inscrire"), ("Visiteur", "Se connecter"), ("Visiteur", "Se déconnecter"),
     ("Visiteur", "Mot de passe oublié")])
uc_diagram(f"{OUT}/fig26_uc_users.png", "Diagramme du cas d'utilisation « Gérer les utilisateurs »",
    ["Administrateur"], [],
    ["Consulter la liste", "Ajouter un utilisateur", "Modifier un utilisateur",
     "Supprimer un utilisateur", "Changer le rôle"],
    [("Administrateur", "Consulter la liste"), ("Administrateur", "Ajouter un utilisateur"),
     ("Administrateur", "Modifier un utilisateur"), ("Administrateur", "Supprimer un utilisateur"),
     ("Administrateur", "Changer le rôle")])
uc_diagram(f"{OUT}/fig27_uc_dashboard.png", "Diagramme du cas d'utilisation « Consulter le tableau de bord »",
    ["Administrateur", "Support"], [],
    ["Voir les indicateurs", "Voir la file d'attention", "Exporter les commandes"],
    [("Administrateur", "Voir les indicateurs"), ("Administrateur", "Voir la file d'attention"),
     ("Administrateur", "Exporter les commandes"), ("Support", "Voir les indicateurs"),
     ("Support", "Voir la file d'attention")])
uc_diagram(f"{OUT}/fig28_uc_brands.png", "Diagramme du cas d'utilisation « Gérer les marques et univers »",
    ["Administrateur"], [],
    ["Lister marques & univers", "Ajouter une marque", "Modifier un univers", "Mettre en avant"],
    [("Administrateur", "Lister marques & univers"), ("Administrateur", "Ajouter une marque"),
     ("Administrateur", "Modifier un univers"), ("Administrateur", "Mettre en avant")])

# ── Fig 29 : classes sprint 1 ──────────────────────────────
f, ax = fig(6.6, 4.4)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
title(ax, "Diagramme de classes — sprint 1 (socle)")
class_box(ax, 0.3, 4.9, 3.0, 3.4, "User",
    ["+ id : int", "+ email : string", "+ passwordHash", "+ firstName, lastName", "+ phone : string", "+ role : enum", "+ loyaltyPoints : int"],
    ["+ hasRole() : bool"], BLUE_L)
class_box(ax, 3.6, 4.9, 3.0, 3.4, "Session",
    ["+ id : string(64)", "+ userId : int FK", "+ expiresAt : date", "+ userAgent : string"],
    ["+ isExpired() : bool"], BLUE_L)
class_box(ax, 6.9, 4.9, 2.9, 3.4, "Address",
    ["+ userId : int FK", "+ fullName, phone", "+ line1, city", "+ governorate", "+ isDefault : bool"], None, SHADE)
class_box(ax, 0.3, 1.1, 3.0, 2.9, "Brand",
    ["+ slug : string", "+ name, country", "+ story : text", "+ isFeatured : bool"], None, GOLD_L)
class_box(ax, 3.6, 1.1, 3.0, 2.9, "Category",
    ["+ slug, name", "+ isUniverse : bool", "+ parentId : int?", "+ sortOrder : int"], None, GOLD_L)
class_box(ax, 6.9, 1.1, 2.9, 2.9, "AuditLog",
    ["+ actorId : int?", "+ action, entity", "+ entityId, details"], None, SHADE)
arrow(ax, (3.3, 6.6), (3.6, 6.6), "1 — *", fs=7)
arrow(ax, (3.3, 5.9), (6.9, 5.9), "", fs=7)  # user-address
ax.text(5.1, 6.0, "1 — *", fontsize=7, color=MUTED)
save(f, f"{OUT}/fig29_classes_s1.png")

# ── Figs 30-34 : séquences sprint 1 ────────────────────────
seq_diagram(f"{OUT}/fig30_seq_auth.png", "Diagramme de séquence « S'authentifier »",
    ["Visiteur", "Page /connexion", "loginAction", "PostgreSQL"],
    [(0, 1, "saisir e-mail + mot de passe", False), (1, 2, "loginAction(form)", False),
     (2, 2, "checkOrigin + rateLimit", False), (2, 3, "SELECT user by email", False),
     (3, 2, "user / null", True), (2, 2, "verifyPassword (scrypt)", False),
     (2, 3, "INSERT session", False), (2, 1, "cookie httpOnly + redirect", True)])
seq_diagram(f"{OUT}/fig31_seq_adduser.png", "Diagramme de séquence « Ajouter un utilisateur »",
    ["Admin", "Form. utilisateur", "saveUserAction", "PostgreSQL"],
    [(0, 1, "remplir le formulaire", False), (1, 2, "saveUserAction(form)", False),
     (2, 2, "requireAdmin + Zod", False), (2, 3, "SELECT email existant ?", False),
     (3, 2, "aucun doublon", True), (2, 2, "hashPassword(scrypt)", False),
     (2, 3, "INSERT user + audit", False), (2, 1, "ok : compte créé", True)])
seq_diagram(f"{OUT}/fig32_seq_edituser.png", "Diagramme de séquence « Modifier un utilisateur »",
    ["Admin", "Fiche client", "saveUserAction", "PostgreSQL"],
    [(0, 1, "éditer rôle / note", False), (1, 2, "updateUserRoleAction()", False),
     (2, 2, "requireAdmin + anti auto-rétrogradation", False), (2, 3, "UPDATE users", False),
     (2, 3, "INSERT audit_logs", False), (2, 1, "ok : rôle mis à jour", True)])
seq_diagram(f"{OUT}/fig33_seq_deluser.png", "Diagramme de séquence « Supprimer un utilisateur »",
    ["Admin", "Fiche client", "deleteUserAction", "PostgreSQL"],
    [(0, 1, "cliquer Supprimer", False), (1, 0, "dialogue de confirmation", True),
     (0, 1, "confirmer", False), (1, 2, "deleteUserAction(id)", False),
     (2, 2, "requireAdmin + contrôle", False), (2, 3, "DELETE (cascade sessions)", False),
     (2, 1, "ok + revalidation", True)])
seq_diagram(f"{OUT}/fig34_seq_listusers.png", "Diagramme de séquence « Consulter la liste des utilisateurs »",
    ["Admin", "Page /admin/clients", "Server Component", "PostgreSQL"],
    [(0, 1, "ouvrir la page", False), (1, 2, "getCurrentUser()", False),
     (2, 2, "requireStaff()", False), (2, 3, "SELECT users + commandes", False),
     (3, 2, "lignes paginées", True), (2, 1, "rendu HTML", True)])

# ── Figs 35-44 : interfaces sprint 1 ───────────────────────
# 35 connexion
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/connexion"); mtopnav(ax)
mtext(ax, 5, 6.9, "Bon retour parmi nous", fs=10, bold=True, ha="center")
mtext(ax, 5, 6.45, "Connectez-vous pour suivre vos commandes et vos favoris.", fs=6.8, color=M_SUB, ha="center")
mfield(ax, 3.1, 5.15, 3.8, 0.5, "Adresse e-mail", "ines.mansour@mail.tn")
mfield(ax, 3.1, 4.15, 3.8, 0.5, "Mot de passe", "••••••••••")
mtext(ax, 6.9, 3.75, "Mot de passe oublié ?", fs=6.3, color=M_ACC, ha="right")
mbtn(ax, 3.1, 2.95, 3.8, 0.55, "Se connecter")
mtext(ax, 5, 2.45, "Pas encore de compte ?  Créer un compte", fs=6.5, ha="center")
mtext(ax, 5, 1.95, "Connexion sécurisée — mot de passe haché (scrypt), session httpOnly de 30 jours.", fs=6, color=M_SUB, ha="center", italic=True)
mtext(ax, 5, 1.0, "Maquette — page de connexion", fs=6.5, color=M_SUB, ha="center", italic=True)
save(f, f"{OUT}/fig35_login.png")

# 36 liste utilisateurs
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/clients"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Clientes & clients", "Support", "Journal d'audit"], 2)
mtext(ax, 2.5, 8.0, "Clientes & clients", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "1 248 comptes · recherche par nom ou e-mail", fs=6.8, color=M_SUB)
mbtn(ax, 8.35, 7.55, 1.3, 0.45, "+ Utilisateur", fs=6)
mtable(ax, 2.5, 6.3, 7.15, ["Nom", "E-mail", "Rôle", "Cmds", ""],
       [["Ines Mansour", "ines.m@mail.tn", "Cliente", "6", "Voir"],
        ["Sami Trabelsi", "sami.t@mail.tn", "Support", "—", "Voir"],
        ["Nour Ben Salah", "nour.b@mail.tn", "Admin", "—", "Voir"],
        ["Amira Belhaj", "amira.b@mail.tn", "Cliente", "2", "Voir"]],
       colw=[1.7, 1.9, 1.15, 0.7, 0.71])
mtext(ax, 2.5, 3.15, "◀  1  2  3  …  52  ▶", fs=6.5, color=M_SUB)
save(f, f"{OUT}/fig36_users_list.png")

# 37 ajout utilisateur
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/clients/nouveau"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Clientes & clients", "Support"], 2)
mtext(ax, 2.5, 8.0, "Nouvel utilisateur", fs=10, bold=True)
mfield(ax, 2.5, 6.9, 3.4, 0.48, "Prénom", "Yasmine")
mfield(ax, 6.1, 6.9, 3.4, 0.48, "Nom", "Khelifi")
mfield(ax, 2.5, 5.9, 3.4, 0.48, "E-mail", "yasmine.k@mail.tn")
mfield(ax, 6.1, 5.9, 3.4, 0.48, "Téléphone", "22 345 678")
mfield(ax, 2.5, 4.9, 3.4, 0.48, "Mot de passe provisoire", "••••••••")
mfield(ax, 6.1, 4.9, 3.4, 0.48, "Rôle", "Cliente ▾")
mbtn(ax, 2.5, 3.9, 1.8, 0.5, "Créer le compte")
mbtn(ax, 4.5, 3.9, 1.5, 0.5, "Annuler", primary=False)
mtext(ax, 2.5, 3.3, "Le mot de passe est haché en scrypt avant stockage ; un e-mail de bienvenue est proposé.", fs=6, color=M_SUB, italic=True)
save(f, f"{OUT}/fig37_user_add.png")

# 38 modif / suppression
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/clients/12"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Clientes & clients"], 2)
mtext(ax, 2.5, 8.0, "Ines Mansour", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "ines.m@mail.tn · Cliente depuis le 12/03/2025 · 42 points fidélité", fs=6.8, color=M_SUB)
mfield(ax, 2.5, 6.5, 3.4, 0.48, "Rôle", "Cliente ▾")
mfield(ax, 6.1, 6.5, 3.4, 0.48, "Téléphone", "22 345 678")
mfield(ax, 2.5, 5.5, 7.0, 0.9, "Note interne (équipe uniquement)", "Préfère la livraison à Ezzahra. Offrir un échantillon solaire.")
mbtn(ax, 2.5, 4.6, 1.8, 0.5, "Enregistrer")
ax.add_patch(FancyBboxPatch((4.5, 4.6), 1.8, 0.5, boxstyle="round,pad=0.01,rounding_size=0.08", fc="white", ec="#A34A3E", lw=1))
ax.text(5.4, 4.85, "Supprimer", ha="center", va="center", fontsize=6.5, color="#A34A3E", weight="bold")
mtext(ax, 2.5, 4.0, "Historique : 6 commandes · 3 avis · dernière visite il y a 2 jours.", fs=6.3, color=M_SUB)
save(f, f"{OUT}/fig38_user_edit.png")

# 39 dialogue suppression
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/clients/12"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Clientes & clients"], 2)
mtext(ax, 2.5, 8.0, "Ines Mansour", fs=10, bold=True, color="#B9B0A0")
ax.add_patch(Rectangle((0.15, 0.35), 9.7, 9.05, fc="#2B2620", ec="none", alpha=0.35))
ax.add_patch(FancyBboxPatch((2.6, 3.4), 4.8, 2.6, boxstyle="round,pad=0.02,rounding_size=0.12", fc="white", ec=M_LINE, lw=1.1))
mtext(ax, 5, 5.55, "Supprimer ce compte ?", fs=8.5, bold=True, ha="center")
mtext(ax, 5, 5.05, "Le compte, ses sessions et ses adresses", fs=6.6, ha="center")
mtext(ax, 5, 4.7, "seront définitivement supprimés.", fs=6.6, ha="center")
mbtn(ax, 3.0, 3.8, 1.9, 0.5, "Annuler", primary=False)
ax.add_patch(FancyBboxPatch((5.1, 3.8), 1.9, 0.5, boxstyle="round,pad=0.01,rounding_size=0.08", fc="#A34A3E", ec="#A34A3E"))
ax.text(6.05, 4.05, "Supprimer", ha="center", va="center", fontsize=6.5, color="white", weight="bold")
save(f, f"{OUT}/fig39_user_delete.png")

# 40 liste marques
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/catalogue/marques"); msidebar(ax, ["Vue d'ensemble", "Produits", "Marques & univers", "Stock"], 2)
mtext(ax, 2.5, 8.0, "Marques & univers", fs=10, bold=True)
mbtn(ax, 8.35, 7.55, 1.3, 0.45, "+ Marque", fs=6)
mtable(ax, 2.5, 6.6, 7.15, ["Marque", "Pays", "Produits", "Vedette", ""],
       [["La Roche-Posay", "France", "14", "★ Oui", "Éditer"],
        ["Avène", "France", "11", "★ Oui", "Éditer"],
        ["Vichy", "France", "9", "★ Oui", "Éditer"],
        ["Bioderma", "France", "8", "—", "Éditer"],
        ["Nuxe", "France", "6", "★ Oui", "Éditer"]],
       colw=[1.8, 1.1, 1.15, 1.1, 1.0])
mtext(ax, 2.5, 3.35, "Univers : Visage · Corps · Cheveux · Solaire · Bébé & Maman · Compléments · Hygiène", fs=6.3, color=M_SUB)
save(f, f"{OUT}/fig40_brands_list.png")

# 41 ajout marque
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/catalogue/marques/nouveau"); msidebar(ax, ["Vue d'ensemble", "Produits", "Marques & univers"], 2)
mtext(ax, 2.5, 8.0, "Nouvelle marque", fs=10, bold=True)
mfield(ax, 2.5, 6.9, 3.4, 0.48, "Nom", "CeraVe")
mfield(ax, 6.1, 6.9, 3.4, 0.48, "Pays", "États-Unis")
mfield(ax, 2.5, 5.9, 7.0, 0.9, "Histoire de la marque", "Développée avec des dermatologues, trois céramides essentiels…")
mtext(ax, 2.5, 5.35, "☑  Mettre en avant sur la page d'accueil", fs=6.6)
mbtn(ax, 2.5, 4.5, 1.8, 0.5, "Enregistrer")
mbtn(ax, 4.5, 4.5, 1.5, 0.5, "Annuler", primary=False)
save(f, f"{OUT}/fig41_brand_add.png")

# 42 modif univers
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin/catalogue/univers/solaire"); msidebar(ax, ["Vue d'ensemble", "Produits", "Marques & univers"], 2)
mtext(ax, 2.5, 8.0, "Univers « Solaire »", fs=10, bold=True)
mfield(ax, 2.5, 6.9, 3.4, 0.48, "Nom", "Solaire")
mfield(ax, 6.1, 6.9, 3.4, 0.48, "Ordre d'affichage", "4")
mfield(ax, 2.5, 5.9, 7.0, 0.9, "Texte éditorial", "Sous le soleil tunisien, la protection n'est pas une option…")
mtext(ax, 2.5, 5.35, "Catégories rattachées : Protection visage · Protection corps · Après-soleil · Enfants", fs=6.3, color=M_SUB)
mbtn(ax, 2.5, 4.5, 1.8, 0.5, "Enregistrer")
mbtn(ax, 4.5, 4.5, 1.5, 0.5, "Annuler", primary=False)
save(f, f"{OUT}/fig42_universe_edit.png")

# 43 dashboard v1
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Produits", "Support"], 0)
mtext(ax, 2.5, 8.0, "Vue d'ensemble", fs=10, bold=True)
mtext(ax, 2.5, 7.6, "Bonjour Nour · lundi 7 septembre · Ce qui se passe dans la maison, en un regard.", fs=6.5, color=M_SUB)
mkpi(ax, 2.5, 6.2, 1.7, "CA · 30 j", "18 420 DT", "132 commandes")
mkpi(ax, 4.35, 6.2, 1.7, "Panier moyen", "139,500 DT", "30 derniers jours")
mkpi(ax, 6.2, 6.2, 1.7, "À confirmer", "7", "priorité : appel client")
mkpi(ax, 8.05, 6.2, 1.6, "File d'attention", "14", "avis · tickets · stocks")
mtext(ax, 2.5, 5.75, "Actions rapides :   [+ Produit]   [Commandes]   [Modération]   [Support]   [Exporter CSV]", fs=6.3, color=M_ACC)
mtext(ax, 2.5, 5.1, "Dernières commandes", fs=7.5, bold=True)
mtable(ax, 2.5, 4.1, 7.15, ["N°", "Cliente", "Total", "Statut"],
       [["CL-260907-X7K2", "Ines M.", "86,400 DT", "En attente"],
        ["CL-260906-P9D4", "Amira B.", "52,900 DT", "Confirmée"],
        ["CL-260906-M2T8", "Salma R.", "124,000 DT", "Expédiée"]],
       colw=[2.0, 1.6, 1.5, 2.05], rh=0.46)
save(f, f"{OUT}/fig43_dashboard1.png")

# 44 dashboard v2 (file d'attention)
f, ax = fig(6.6, 4.4); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
browser(ax, "cleopatre.tn/admin"); msidebar(ax, ["Vue d'ensemble", "Commandes", "Produits", "Support"], 0)
mtext(ax, 2.5, 8.0, "File d'attention", fs=10, bold=True)
mtext(ax, 2.5, 5.1 - 2.55, "", fs=1)  # spacer
# three panels
for i, (t, rows) in enumerate([
    ("À traiter — commandes", ["CL-260907-X7K2 · 86,400 DT", "CL-260907-Q3N9 · 41,200 DT", "Toutes les en attente →"]),
    ("Alertes stock", ["Effaclar Duo+ · 2 restants", "Anthelios Fluide · 3 restants", "Voir le stock →"]),
    ("Modération & support", ["4 avis en attente", "3 tickets ouverts", "Voir la file →"])]):
    x = 2.5 + i * 2.45
    ax.add_patch(FancyBboxPatch((x, 4.6), 2.3, 2.6, boxstyle="round,pad=0.01,rounding_size=0.1", fc="white", ec=M_LINE, lw=0.9))
    mtext(ax, x + 0.15, 6.95, t, fs=6.3, bold=True)
    y = 6.5
    for r in rows:
        mtext(ax, x + 0.15, y, "• " + r, fs=6.0, color=M_ACC if "→" in r else M_TXT)
        y -= 0.42
mtext(ax, 2.5, 7.6, "Tout ce qui attend une action humaine, réuni en un seul regard.", fs=6.8, color=M_SUB)
mtext(ax, 2.5, 4.1, "Courbe des ventes (30 j) : ▁▂▃▅▃▆▇▆▉▇█▉  — progression +18 % vs mois précédent.", fs=6.3, color=M_SUB)
save(f, f"{OUT}/fig44_dashboard2.png")

print("figs2 done")
