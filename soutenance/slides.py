"""Diaporama de soutenance PFE — Cléopâtre. Thème sombre premium, transitions Morph réelles (p159)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "..", "rapport", "figs")
OUT = os.path.join(HERE, "Soutenance_PFE_Cleopatre.pptx")

# ── thème ────────────────────────────────────────────────
BG = RGBColor(0x20, 0x1A, 0x13)
PANEL = RGBColor(0x2C, 0x25, 0x1B)
PANEL2 = RGBColor(0x36, 0x2D, 0x20)
TXT = RGBColor(0xF3, 0xEC, 0xDD)
MUT = RGBColor(0xB9, 0xAC, 0x93)
GOLD = RGBColor(0xC9, 0xA9, 0x59)
GOLD_D = RGBColor(0x9A, 0x7B, 0x3F)
GHOST_GOLD = RGBColor(0x5A, 0x4C, 0x24)
INK = RGBColor(0x1A, 0x15, 0x10)
SERIF, SANS = "Georgia", "Calibri"
W, H = 13.333, 7.5

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W), Inches(H)
BLANK = prs.slide_layouts[6]


def morph(slide, dur="900"):
    """Injecte une vraie transition Morph (p159, option byObject) + repli fondu."""
    MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
    P = "http://schemas.openxmlformats.org/presentationml/2006/main"
    P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
    P159 = "http://schemas.microsoft.com/office/powerpoint/2015/09/main"
    sld = slide._element
    idx = 0
    for i, ch in enumerate(sld):
        if ch.tag in (f"{{{P}}}cSld", f"{{{P}}}clrMapOvr"):
            idx = i + 1
    ac = etree.Element(f"{{{MC}}}AlternateContent",
                       nsmap={"mc": MC, "p": P, "p14": P14, "p159": P159})
    choice = etree.SubElement(ac, f"{{{MC}}}Choice", Requires="p159")
    tr = etree.SubElement(choice, f"{{{P}}}transition", spd="med", advOnClk="1")
    tr.set(f"{{{P14}}}dur", dur)
    etree.SubElement(tr, f"{{{P159}}}morph", option="byObject")
    fb = etree.SubElement(ac, f"{{{MC}}}Fallback")
    tr2 = etree.SubElement(fb, f"{{{P}}}transition", spd="med")
    etree.SubElement(tr2, f"{{{P}}}fade", thruBlk="1")
    sld.insert(idx, ac)


def bg(slide, name="!!BG"):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    s.name = name
    s.fill.solid()
    s.fill.fore_color.rgb = BG
    s.line.fill.background()
    return s


def txt(slide, l, t, w, h, runs, size=18, name=None, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, color=TXT, font=SANS, bold=False, italic=False, space=6):
    """runs: str ou liste de (texte, dict_opts)."""
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    if isinstance(runs, str):
        runs = [(runs, {})]
    for j, (st, opts) in enumerate(runs):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space)
        for chunk in st.split("\n"):
            r = p.add_run()
            r.text = chunk if chunk else " "
            f = r.font
            f.name = opts.get("font", font)
            f.size = Pt(opts.get("size", size))
            f.bold = opts.get("bold", bold)
            f.italic = opts.get("italic", italic)
            f.color.rgb = opts.get("color", color)
            if chunk != st.split("\n")[-1]:
                p.add_line_break()
    return tb


def panel(slide, l, t, w, h, fill=PANEL, name=None):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    if name:
        s.name = name
    s.adjustments[0] = 0.07
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.color.rgb = GOLD_D
    s.line.width = Pt(1)
    return s


def rule(slide, l, t, w, name="!!RULE"):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Pt(3))
    s.name = name
    s.fill.solid()
    s.fill.fore_color.rgb = GOLD
    s.line.fill.background()
    return s


def header(slide, eyebrow, title):
    txt(slide, 0.7, 0.32, 10.4, 0.36, eyebrow, size=13, name="!!EYE",
        color=GOLD, bold=True, font=SANS, space=2)
    txt(slide, 0.7, 0.72, 10.4, 0.9, title, size=30, name="!!TITLE",
        color=TXT, bold=True, font=SERIF, space=2)
    rule(slide, 0.7, 1.62, 1.6)
    num = eyebrow[:2] if eyebrow[:2].isdigit() else (eyebrow[7:9] if eyebrow.startswith("ANNEXE") else "")
    if num:
        txt(slide, 11.25, 0.28, 1.45, 1.3, num.strip(), size=52, name="!!GHOST",
            color=GHOST_GOLD, bold=True, font=SERIF, align=PP_ALIGN.RIGHT, space=0)


def footer(slide, i, n):
    txt(slide, 0.7, 7.02, 6, 0.35, "Cléopâtre · Soutenance PFE", size=11, name="!!FOOT", color=MUT)
    txt(slide, 12.0, 7.02, 0.7, 0.35, f"{i:02d}", size=11, name="!!NUM", color=MUT, align=PP_ALIGN.RIGHT)


def footer_annex(slide, tag):
    txt(slide, 0.7, 7.02, 6, 0.35, "Cléopâtre · Soutenance PFE — Annexe jury", size=11,
        name="!!FOOT", color=MUT)
    txt(slide, 12.0, 7.02, 0.7, 0.35, tag, size=11, name="!!NUM", color=MUT, align=PP_ALIGN.RIGHT)


def frame(slide):
    for inset, wdt in ((0.16, 2.0), (0.26, 0.75)):
        fr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(inset), Inches(inset),
                                    Inches(W - 2 * inset), Inches(H - 2 * inset))
        fr.name = "!!FRAME"
        fr.fill.background()
        fr.line.color.rgb = GOLD
        fr.line.width = Pt(wdt)


def pic_fit(slide, path, l, t, w, h, name=None, border=True):
    """Image centrée dans la zone (l,t,w,h), ratio conservé. Retourne None si absente."""
    full = os.path.join(FIGS, path)
    if not os.path.exists(full):
        print(f"WARN image manquante : {path}")
        txt(slide, l, t, w, h, f"[image : {path}]", size=12, color=MUT, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)
        return None
    iw, ih = Image.open(full).size
    scale = min(w / iw, h / ih)
    nw, nh = iw * scale, ih * scale
    p = slide.shapes.add_picture(full, Inches(l + (w - nw) / 2), Inches(t + (h - nh) / 2),
                                 Inches(nw), Inches(nh))
    if name:
        p.name = name
    if border:
        p.line.color.rgb = GOLD_D
        p.line.width = Pt(1.25)
    # coins arrondis (Crop to Shape > Rounded Rectangle)
    A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    spPr = p._element.find(qn("p:spPr"))
    old = spPr.find(f"{{{A}}}prstGeom")
    if old is not None:
        spPr.remove(old)
    prst = etree.SubElement(spPr, f"{{{A}}}prstGeom", prst="roundRect")
    av = etree.SubElement(prst, f"{{{A}}}avLst")
    etree.SubElement(av, f"{{{A}}}gd", name="adj", fmla="val 9000")
    return p


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


NSLIDES = 19
C = "•  "  # puce

# ══ 1. Couverture ═════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
frame(s)
pic_fit(s, "fig01_logo.png", 5.92, 0.75, 1.5, 1.5, name="!!LOGO", border=False)
txt(s, 1.0, 2.45, 11.33, 0.5, "RAPPORT DE PROJET DE FIN D'ÉTUDES  ·  SOUTENANCE", size=14,
    name="!!EYE", color=GOLD, bold=True, align=PP_ALIGN.CENTER)
txt(s, 1.0, 2.95, 11.33, 1.6, "Conception et réalisation d'une\nplateforme e-commerce\npour la parapharmacie Cléopâtre",
    size=36, name="!!TITLE", color=TXT, bold=True, font=SERIF, align=PP_ALIGN.CENTER, space=2)
rule(s, 6.17, 4.85, 1.0, name="!!RULE")
txt(s, 1.0, 5.15, 11.33, 1.3,
    [("[Nom Prénom de l'étudiant(e)]", {"size": 17}),
     ("Encadrant académique : [Nom — Grade]      Encadrant professionnel : [Nom — Cléopâtre]", {"size": 13, "color": MUT}),
     ("[Établissement]  ·  Année [20XX–20XX]  ·  [JJ/MM/AAAA]", {"size": 13, "color": MUT})],
    align=PP_ALIGN.CENTER, space=3)
notes(s, "Bonjour. Je vais vous présenter mon Projet de Fin d'Études : la conception et la réalisation "
         "d'une plateforme e-commerce complète pour la parapharmacie Cléopâtre, conduite en méthode Scrum. "
         "Durée prévue : 15 minutes, suivies de vos questions.")

# ══ 2. Plan ═══════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "SOUTENANCE  ·  PLAN", "Cinq temps")
items = [("01", "Contexte & problématique", "La maison, l'existant, la refonte totale"),
         ("02", "Solution & méthode", "Périmètre, Scrum, acteurs, technologies"),
         ("03", "Réalisation", "Sprints 1 à 4 : socle, commerce, relation client, finition"),
         ("04", "Sécurité & fiabilité", "Les 6 garanties non négociables"),
         ("05", "Bilan & perspectives", "Chiffres, démonstration, trajectoire")]
for j, (num, t1, t2) in enumerate(items):
    y = 2.05 + j * 1.02
    panel(s, 2.3, y, 8.73, 0.88, name=f"PLAN{j}")
    txt(s, 2.6, y + 0.08, 1.0, 0.72, num, size=26, color=GOLD, bold=True, font=SERIF)
    txt(s, 3.7, y + 0.06, 7.0, 0.76, [(t1, {"size": 19, "bold": True}),
                                      (t2, {"size": 14, "color": MUT})], space=1)
footer(s, 2, NSLIDES)
notes(s, "Mon exposé suit cinq temps : le contexte, la solution et la méthode, la réalisation sprint par "
         "sprint, les garanties de sécurité, puis le bilan et les perspectives.")

# ══ 3. Contexte ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "01  ·  CONTEXTE", "La maison Cléopâtre")
pic_fit(s, "fig01_logo.png", 0.7, 2.1, 2.2, 2.2, name="!!LOGO", border=False)
cards = [("2", "boutiques", "Ezzahra\nHammam-Lif"), ("80", "références", "7 univers\n15 marques"),
         ("0", "canal digital", "ni site marchand\nni données")]
for j, (n, t1, t2) in enumerate(cards):
    x = 3.3 + j * 3.2
    panel(s, x, 2.15, 2.9, 2.6, name=f"CTX{j}")
    txt(s, x + 0.25, 2.3, 2.4, 2.3, [(n, {"size": 44, "bold": True, "color": GOLD, "font": SERIF}),
                                     (t1, {"size": 18, "bold": True}),
                                     (t2, {"size": 14, "color": MUT})], align=PP_ALIGN.CENTER, space=2)
txt(s, 0.7, 5.15, 11.9, 1.5,
    "Positionnement : le conseil pharmaceutique exigeant — écoute, diagnostic, recommandation.\nRéputation locale excellente, mais clientèle exclusivement « physique ».",
    size=16, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 3, NSLIDES)
notes(s, "Cléopâtre, Espace Santé Beauté : deux boutiques à Ezzahra et Hammam-Lif, 80 références, "
         "positionnement conseil. Mais aucun canal digital : pas de catalogue à distance, pas de données.")

# ══ 4. Problématique ══════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "01  ·  PROBLÉMATIQUE", "Quatre problèmes, une décision")
pains = [("Perte de CA", "Invisible sur Google :\nles prospects achètent ailleurs."),
         ("Stocks à l'aveugle", "Ruptures découvertes\nau moment de la vente."),
         ("Processus non tracés", "Commandes, remises, retours :\naucune preuve, aucune reprise."),
         ("Pilotage impossible", "Ni panier moyen, ni top ventes :\ndécisions à l'intuition.")]
for j, (t1, t2) in enumerate(pains):
    x = 0.7 + j * 3.05
    panel(s, x, 2.05, 2.85, 2.5, name=f"PB{j}")
    txt(s, x + 0.2, 2.2, 2.45, 2.2, [(t1, {"size": 17, "bold": True, "color": GOLD}),
                                     (t2, {"size": 14, "color": TXT})], align=PP_ALIGN.CENTER, space=4)
panel(s, 0.7, 4.85, 11.93, 1.85, fill=PANEL2, name="REFONTE")
txt(s, 1.0, 5.0, 11.33, 1.6, [("Décision : refonte totale — reconstruit de zéro", {"size": 19, "bold": True}),
                               ("Ancien site vitrine sans vente ni gestion → nouveau socle, nouveau modèle, nouvelles interfaces. Zéro reprise de code. Comparatif page à page : Annexe A du rapport.",
                                {"size": 14, "color": MUT})], align=PP_ALIGN.CENTER, space=4)
footer(s, 4, NSLIDES)
notes(s, "Quatre problèmes critiques, du manque à gagner à l'impossibilité de piloter. Face à l'ancien "
         "site vitrine, la direction a tranché : pas d'évolution, une reconstruction totale. Le comparatif "
         "avant-après est documenté en Annexe A.")

# ══ 5. Solution ═══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "02  ·  SOLUTION", "Une plateforme, deux visages")
panel(s, 0.7, 2.0, 5.85, 4.7, name="SOL0")
txt(s, 1.0, 2.15, 5.25, 4.4, [("Site marchand — public", {"size": 19, "bold": True, "color": GOLD}),
                               (C + "Catalogue : 81 produits, 7 univers, 15 marques\n" + C + "Recherche à facettes, fiches, avis vérifiés\n" + C + "Panier, tunnel 4 étapes, paiement livraison\n" + C + "Compte client + suivi invité sécurisé", {"size": 15})], space=4)
panel(s, 6.78, 2.0, 5.85, 4.7, name="SOL1")
txt(s, 7.08, 2.15, 5.25, 4.4, [("Back-office — staff", {"size": 19, "bold": True, "color": GOLD}),
                                (C + "Dashboard : KPI + file d'attention\n" + C + "Commandes, stock, promotions, clients\n" + C + "Avis, tickets support, journal, audit\n" + C + "Rôles admin / support, exports CSV", {"size": 15})], space=4)
footer(s, 5, NSLIDES)
notes(s, "La solution : une plateforme intégrée, une seule base de données, deux visages. Côté public, "
         "un site marchand raffiné. Côté privé, un back-office qui outille les trois missions : "
         "avant-vente, vente, après-vente.")

# ══ 6. Scrum ══════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "02  ·  MÉTHODE", "Scrum : 1 cadrage + 4 sprints, 2 releases")
pic_fit(s, "fig03_scrum.png", 0.7, 2.0, 5.6, 4.2, name="SCRUM")
panel(s, 6.6, 2.0, 2.75, 4.2, name="REL1")
txt(s, 6.8, 2.15, 2.35, 3.9, [("Release 1", {"size": 18, "bold": True, "color": GOLD}),
                               ("Cœur marchand", {"size": 14, "bold": True}),
                               ("S1 — Socle\nS2 — Commerce", {"size": 14, "color": MUT})], align=PP_ALIGN.CENTER)
panel(s, 9.6, 2.0, 3.03, 4.2, name="REL2")
txt(s, 9.8, 2.15, 2.63, 3.9, [("Release 2", {"size": 18, "bold": True, "color": GOLD}),
                               ("Plateforme complète", {"size": 14, "bold": True}),
                               ("S3 — Relation client\nS4 — Recherche + finition", {"size": 14, "color": MUT})],
    align=PP_ALIGN.CENTER)
txt(s, 6.6, 6.35, 6.03, 0.5, "Sprint 0 : acteurs, besoins, backlog (24 récits), planning, stack.",
    size=13, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 6, NSLIDES)
notes(s, "Méthode Scrum : un sprint 0 de cadrage, puis deux releases de deux sprints de deux semaines. "
         "Chaque sprint se termine par une démonstration réelle à la direction.")

# ══ 7. Acteurs & besoins ══════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "02  ·  BESOINS", "5 acteurs, 8 domaines, 24 récits")
acts = ["Visiteur", "Client", "Invité", "Support", "Admin"]
for j, a in enumerate(acts):
    panel(s, 0.7 + j * 2.45, 2.0, 2.2, 1.05, name=f"ACT{j}")
    txt(s, 0.7 + j * 2.45, 2.18, 2.2, 0.7, a, size=17, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
txt(s, 0.7, 3.35, 11.93, 3.3,
    C + "Compte & fidélité   " + C + "Catalogue & stock   " + C + "Commandes & suivi\n" +
    C + "Promotions   " + C + "Avis & support   " + C + "Recherche & journal\n" +
    C + "Administration & audit   " + C + "Exigences : sécurité, fiabilité, performance",
    size=16, space=8)
footer(s, 7, NSLIDES)
notes(s, "Cinq acteurs aux droits cumulatifs, huit domaines fonctionnels, 24 récits utilisateurs chiffrés "
         "et planifiés. Les exigences non fonctionnelles — sécurité, fiabilité — irriguent tous les sprints.")

# ══ 8. Stack ══════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "02  ·  TECHNOLOGIES", "Une stack moderne, typée de bout en bout")
techs = [("Next.js 16", "Framework\nfull-stack"), ("React 19", "Interfaces\nserveur + client"),
         ("TypeScript", "Typage strict\nzéro any"), ("PostgreSQL 18", "24 tables\nACID"),
         ("Drizzle", "ORM\nprofils SQL"), ("Zod", "Validation\nserveur"), ("scrypt", "Mots de passe\nsalés"),
         ("Docker", "Build & run\nreproductibles")]
for j, (t1, t2) in enumerate(techs):
    x, y = 0.7 + (j % 4) * 3.05, 2.0 + (j // 4) * 2.35
    panel(s, x, y, 2.85, 2.05, name=f"TEC{j}")
    txt(s, x + 0.15, y + 0.15, 2.55, 1.75, [(t1, {"size": 18, "bold": True, "color": GOLD}),
                                            (t2, {"size": 14, "color": MUT})], align=PP_ALIGN.CENTER, space=3)
footer(s, 8, NSLIDES)
notes(s, "Stack JavaScript moderne : Next.js et React pour le full-stack, TypeScript strict, PostgreSQL "
         "via Drizzle, validation Zod systématique, hachage scrypt, conteneurisation Docker.")

# ══ 9. Architecture ═══════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "02  ·  ARCHITECTURE", "Trois couches, un seul socle de vérité")
pic_fit(s, "fig20_archilogicielle.png", 1.5, 1.9, 10.33, 4.85, name="ARCHI")
footer(s, 9, NSLIDES)
notes(s, "Architecture en couches : présentation, actions serveur validées, services métier, base unique. "
         "Vitrine et back-office partagent les mêmes règles : un seul socle de vérité.")

# ══ 10. Modèle ════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "02  ·  MODÈLE DE DONNÉES", "24 tables, 10 énumérations, zéro incohérence")
pic_fit(s, "figR1_modele.png", 0.7, 1.9, 7.6, 4.85, name="MODELE")
panel(s, 8.6, 1.9, 4.03, 4.85, name="MODSTATS")
txt(s, 8.85, 2.05, 3.53, 4.55, [("24", {"size": 40, "bold": True, "color": GOLD, "font": SERIF}),
                                 ("tables + 10 énumérations", {"size": 15, "bold": True}),
                                 ("Montants en millimes\nUnicités en base\nCascades référentielles\nTransactions verrouillées",
                                  {"size": 14, "color": MUT})], align=PP_ALIGN.CENTER, space=3)
footer(s, 10, NSLIDES)
notes(s, "Le modèle consolidé : 24 tables, 10 énumérations. Les règles d'intégrité vivent dans la base, "
         "pas seulement dans le code : montants entiers en millimes, unicités, cascades, transactions.")

# ══ 11. Sprint 1 ══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "03  ·  SPRINT 1 — SOCLE", "Connexion sécurisée, back-office, référentiels")
pic_fit(s, "fig35_login.png", 0.7, 1.95, 5.85, 3.4, name="S1A")
pic_fit(s, "fig43_dashboard1.png", 6.78, 1.95, 5.85, 3.4, name="S1B")
txt(s, 0.7, 5.6, 11.93, 1.2,
    "scrypt + sessions httpOnly 256 bits  ·  gardes requireUser / Staff / Admin  ·  anti-brute-force  ·  file d'attention",
    size=14, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 11, NSLIDES)
notes(s, "Sprint 1, le socle : authentification avec scrypt et sessions opaques, hiérarchie des rôles "
         "garantie par des gardes serveur, tableau de bord avec file d'attention.")

# ══ 12. Sprint 2 ══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "03  ·  SPRINT 2 — COMMERCE", "Catalogue, tunnel idempotent, cycle de vie")
pic_fit(s, "fig59_checkout34.png", 0.7, 1.95, 5.85, 3.4, name="S2A")
pic_fit(s, "fig62_suivi.png", 6.78, 1.95, 5.85, 3.4, name="S2B")
txt(s, 0.7, 5.6, 11.93, 1.2,
    "Tunnel 4 étapes validées  ·  anti-double-commande (verrou + clé unique)  ·  machine à états 7 statuts  ·  timeline client",
    size=14, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 12, NSLIDES)
notes(s, "Sprint 2, le commerce : 81 fiches produits, tunnel de commande en quatre étapes, "
         "idempotence anti-double-clic, machine à états des commandes, suivi client en langage simple.")

# ══ 13. Sprint 3 ══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "03  ·  SPRINT 3 — RELATION CLIENT", "Avis vérifiés, support tracé, confiance")
pic_fit(s, "fig69_reviews.png", 0.7, 1.95, 5.85, 3.4, name="S3A")
pic_fit(s, "fig71_ticket_reply.png", 6.78, 1.95, 5.85, 3.4, name="S3B")
txt(s, 0.7, 5.6, 11.93, 1.2,
    "Modération + réponse maison  ·  agrégation atomique (note jamais fausse)  ·  tickets SLA 24 h  ·  anti-spam",
    size=14, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 13, NSLIDES)
notes(s, "Sprint 3, la relation client : avis modérés avec réponse de la maison, note moyenne recalculée "
         "en transaction, réclamations avec délai contractuel de 24 heures.")

# ══ 14. Sprint 4 ══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "03  ·  SPRINT 4 — FINITION", "Recherche, journal, Docker")
pic_fit(s, "fig78_search.png", 0.7, 1.95, 5.85, 3.4, name="S4A")
pic_fit(s, "fig83_docker.png", 6.78, 1.95, 5.85, 3.4, name="S4B")
txt(s, 0.7, 5.6, 11.93, 1.2,
    "Recherche instantanée FR/AR + synonymes  ·  journal pharmaceutique  ·  build multi-stage  ·  seed de démo",
    size=14, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 14, NSLIDES)
notes(s, "Sprint 4, la finition : recherche instantanée multilingue analysée, journal de conseils, "
         "conteneurisation Docker et seed complet pour des recettes reproductibles.")

# ══ 15. Avant / Après ═════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "03  ·  REFONTE", "Avant / Après : rien n'a été conservé")
panel(s, 0.7, 1.95, 5.85, 0.75, name="AVA")
txt(s, 0.7, 2.05, 5.85, 0.55, "AVANT — ancien site", size=17, bold=True, color=MUT, align=PP_ALIGN.CENTER)
pic_fit(s, "avant_accueil.png", 0.7, 2.8, 5.85, 3.3, name="AVANTIMG")
panel(s, 6.78, 1.95, 5.85, 0.75, fill=PANEL2, name="APA")
txt(s, 6.78, 2.05, 5.85, 0.55, "APRÈS — plateforme livrée", size=17, bold=True, color=GOLD,
    align=PP_ALIGN.CENTER)
pic_fit(s, "fig85_home.png", 6.78, 2.8, 5.85, 3.3, name="APRESIMG")
txt(s, 0.7, 6.3, 11.93, 0.5, "Insérez votre capture « avant » dans le cadre de gauche — Annexe A du rapport.",
    size=12, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 15, NSLIDES)
notes(s, "La preuve de la refonte : à gauche l'ancien site vitrine, à droite la plateforme livrée. "
         "Même page, même maison — tout le reste a changé. Le rapport documente six paires en Annexe A.")

# ══ 16. Sécurité ══════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "04  ·  SÉCURITÉ & FIABILITÉ", "Six garanties non négociables")
guars = [("Argent exact", "Millimes entiers\njamais de flottants"),
         ("Secrets protégés", "scrypt salé\nsessions httpOnly"),
         ("Accès contrôlés", "Gardes serveur\nrôles cumulatifs"),
         ("Stocks sûrs", "Verrous FOR UPDATE\njamais négatifs"),
         ("Clics uniques", "Idempotence\nzéro doublon"),
         ("Tout est tracé", "Audit staff\ntimeline client")]
for j, (t1, t2) in enumerate(guars):
    x = 0.7 + (j % 3) * 4.08
    y = 2.0 + (j // 3) * 2.4
    panel(s, x, y, 3.88, 2.1, name=f"SEC{j}")
    txt(s, x + 0.2, y + 0.2, 3.48, 1.7, [(t1, {"size": 18, "bold": True, "color": GOLD}),
                                         (t2, {"size": 14, "color": TXT})], align=PP_ALIGN.CENTER, space=3)
footer(s, 16, NSLIDES)
notes(s, "Six garanties structurent toute la réalisation : argent exact, secrets protégés, accès "
         "contrôlés, stocks sûrs, commandes idempotentes, traçabilité complète. Chacune est démontrée "
         "dans le rapport, code à l'appui.")

# ══ 17. Bilan ═════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "05  ·  BILAN", "Livré, démontré, accepté")
stats = [("24/24", "récits terminés\n2 releases acceptées"), ("81", "produits en ligne\n8 marques, 7 univers"),
         ("24", "tables + audit\n10 énumérations"), ("104", "pages de rapport\n94 figures, 40 tableaux")]
for j, (n, t) in enumerate(stats):
    x = 0.7 + j * 3.05
    panel(s, x, 2.05, 2.85, 2.4, name=f"BIL{j}")
    txt(s, x + 0.2, 2.2, 2.45, 2.1, [(n, {"size": 36, "bold": True, "color": GOLD, "font": SERIF}),
                                     (t, {"size": 14, "color": TXT})], align=PP_ALIGN.CENTER, space=2)
txt(s, 0.7, 4.8, 11.93, 1.7,
    "Démonstrations réelles à chaque revue  ·  recette Docker reproductible  ·  apports personnels : full-stack, Scrum, rédaction",
    size=15, color=MUT, align=PP_ALIGN.CENTER)
footer(s, 17, NSLIDES)
notes(s, "Bilan : les 24 récits sont terminés et démontrés, la recette tourne sous Docker, le rapport "
         "fait 104 pages. Personnellement : autonomie full-stack, rigueur Scrum, et l'exigence d'écrire "
         "un code que l'on peut expliquer au jury.")

# ══ 18. Démo ══════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "05  ·  DÉMONSTRATION", "La preuve par l'écran")
panel(s, 0.7, 2.0, 7.3, 4.7, name="DEMOL")
txt(s, 1.0, 2.15, 6.7, 4.4, [("Scénario — 6 minutes", {"size": 19, "bold": True, "color": GOLD}),
                              ("1. Acheter : recherche « solaire », fiche produit, panier, tunnel, confirmation.\n"
                               "2. Piloter : la commande tombe au dashboard, avance Confirmée → Expédiée.\n"
                               "3. Rassurer : timeline client, avis modéré, ticket support clôturé.",
                               {"size": 15})], space=6)
panel(s, 8.3, 2.0, 4.03, 4.7, name="DEMOR")
txt(s, 8.55, 2.15, 3.53, 4.4, [("Accès recette", {"size": 17, "bold": True, "color": GOLD}),
                                ("[Collez ici le QR]", {"size": 14, "color": MUT}),
                                ("https://[recette].tn", {"size": 14, "bold": True}),
                                ("client : [e-mail] / [mdp]\nadmin : [e-mail] / [mdp]",
                                 {"size": 13, "color": MUT})], align=PP_ALIGN.CENTER, space=5)
footer(s, 18, NSLIDES)
notes(s, "Passons à la démonstration en direct : six minutes, trois actes — acheter, piloter, rassurer. "
         "Le QR et les comptes de recette sont affichés. En cas de réseau capricieux, les captures du "
         "rapport prennent le relais.")

# ══ 19. Merci ═════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
frame(s)
txt(s, 1.0, 1.2, 11.33, 0.35, "05  ·  PERSPECTIVES", size=13, name="!!EYE", color=GOLD, bold=True,
    align=PP_ALIGN.CENTER)
txt(s, 1.0, 1.6, 11.33, 1.0, "Merci de votre attention", size=38, name="!!TITLE", color=TXT, bold=True,
    font=SERIF, align=PP_ALIGN.CENTER)
rule(s, 6.17, 2.75, 1.0, name="!!RULE")
txt(s, 2.5, 3.1, 8.33, 1.3,
    "Paiement en ligne  ·  version arabe complète  ·  recommandations personnalisées  ·  application mobile",
    size=15, color=MUT, align=PP_ALIGN.CENTER)
txt(s, 2.5, 4.5, 8.33, 0.7, "Je réponds à vos questions.", size=22, bold=True, color=GOLD, font=SERIF,
    align=PP_ALIGN.CENTER)
txt(s, 2.5, 5.5, 8.33, 0.9,
    [("[Nom Prénom]  ·  [e-mail]  ·  [téléphone]", {"size": 14, "color": MUT})], align=PP_ALIGN.CENTER)
notes(s, "Conclure : remercier le jury, rappeler les perspectives — paiement en ligne, version arabe, "
         "recommandation — et ouvrir aux questions.")

# ══ A1. Backup : machine à états ══════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "ANNEXE A1  ·  SECOURS JURY", "Cycle de vie d'une commande — machine à états")
pic_fit(s, "fig49_statemachine.png", 1.5, 1.9, 10.33, 4.85, name="BK1")
footer_annex(s, "A1")
notes(s, "Secours : si le jury questionne les transitions — 7 statuts, transitions verrouillées en base, "
         "effets idempotents (paiement COD, fidélité, réassort).")

# ══ A2. Backup : sécurité ═════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "ANNEXE A2  ·  SECOURS JURY", "Sécurité — hachage, sessions, rôles")
pic_fit(s, "fig23_scrypt.png", 0.7, 1.95, 5.85, 4.75, name="BK2A")
pic_fit(s, "fig24_roles.png", 6.78, 1.95, 5.85, 4.75, name="BK2B")
footer_annex(s, "A2")
notes(s, "Secours : si le jury creuse la sécurité — scrypt salé, sessions opaques 256 bits en cookie "
         "httpOnly, gardes serveur cumulatifs, anti-brute-force et anti-énumération.")

# ══ A3. Backup : modèle global ════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "ANNEXE A3  ·  SECOURS JURY", "Modèle global — relation client, contenu, pilotage")
pic_fit(s, "figGX_modele.png", 2.6, 1.9, 8.13, 4.85, name="BK3")
footer_annex(s, "A3")
notes(s, "Secours : si le jury veut le modèle complet — 10 tables autonomes reliées à la release 1, "
         "24 tables et 10 énumérations au total, dictionnaire en Annexe B du rapport.")

# ══ A4. Backup : déploiement ══════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
header(s, "ANNEXE A4  ·  SECOURS JURY", "Mise en production — conteneurs et recette")
pic_fit(s, "fig19_deploiement.png", 1.5, 1.9, 10.33, 4.85, name="BK4")
footer_annex(s, "A4")
notes(s, "Secours : si le jury questionne l'exploitation — conteneurs web + base, variables "
         "d'environnement, seed de démonstration, sauvegardes pg_dump, guide en Annexe C.")

# ── Morph sur chaque diapo + métadonnées + sauvegarde ───
for sl in prs.slides:
    morph(sl)

cp = prs.core_properties
cp.title = "Soutenance PFE — Plateforme e-commerce Cléopâtre"
cp.author = "[Nom Prénom de l'étudiant(e)]"
cp.subject = "Diaporama de soutenance — transitions Morph"
cp.keywords = "PFE, Cléopâtre, e-commerce, Scrum, soutenance"

prs.save(OUT)
print(f"PPTX généré : {OUT} ({len(prs.slides.__iter__.__self__._sldIdLst)} diapos)")
