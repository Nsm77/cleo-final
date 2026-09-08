"""Assemble le rapport PFE complet : garde, sommaire, chapitres, listes, conclusion."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc import Report, INK, MUTED, GOLD, GOLD_DARK, STONE_LINE, SHADE
from content_a import INTRO, CH1
from content_b import CH2
from content_c import CH3
from content_d import CH4
from content_e import FIN, BIBLIO, RESUME, ABBR
from content_f import ANNEXES

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figs")
OUT_PDF = os.path.join(HERE, "Rapport_PFE_Cleopatre.pdf")

BODY = INTRO + CH1 + CH2 + CH3 + CH4 + FIN + BIBLIO + ANNEXES + RESUME


def md(text: str) -> str:
    """Prétraitement markdown fpdf2 : `code` -> gras (une seule famille par bloc)."""
    text = re.sub(r"`([^`]+)`", r"**\1**", text)
    return text


def check_markup():
    for i, (kind, payload) in enumerate(BODY):
        if kind in ("p",):
            for m in re.finditer(r"\*\*", payload):
                pass
            if payload.count("**") % 2:
                print(f"WARN block {i}: ** impair: {payload[:60]}")
            if payload.count("`") % 2:
                print(f"WARN block {i}: ` impair: {payload[:60]}")
        if kind == "bullets":
            for b in payload:
                if b.count("**") % 2 or b.count("`") % 2:
                    print(f"WARN bullet: {b[:60]}")


# ── blocs riches (justifiés) ──────────────────────────────
def paragraph(pdf: Report, text: str):
    for para in text.split("\n"):
        if para.strip() == "":
            pdf.ln(2.5)
            continue
        pdf.set_text_color(*INK)
        pdf.set_font("serif", "", 10.5)
        pdf.multi_cell(0, 5.4, md(para.strip()), markdown=True, align="J")
    pdf.ln(1.6)


def bullets(pdf: Report, items, numbered=False):
    for i, it in enumerate(items, 1):
        pdf.set_font("sans", "B", 10.5)
        pdf.set_text_color(*GOLD_DARK)
        x0 = pdf.l_margin
        pdf.set_x(x0)
        pdf.cell(7, 5.4, f"{i}." if numbered else "•")
        pdf.set_text_color(*INK)
        pdf.set_font("serif", "", 10.5)
        # hanging indent
        x = pdf.get_x()
        w = pdf.w - pdf.r_margin - x
        pdf.multi_cell(w, 5.4, md(it), markdown=True, align="J")
        pdf.ln(0.6)
    pdf.ln(1.5)


# ── pages de garde ────────────────────────────────────────
def cover(pdf: Report):
    pdf.add_page()
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.7)
    pdf.rect(9, 9, 192, 279)
    pdf.set_line_width(0.25)
    pdf.rect(11.5, 11.5, 187, 274)
    pdf.ln(8)
    pdf.set_font("sans", "B", 11)
    pdf.set_text_color(*INK)
    pdf.cell(0, 6, "[ÉTABLISSEMENT — ex. Institut Supérieur d'Informatique]", align="C")
    pdf.ln(6)
    pdf.set_font("sans", "", 10)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 6, "[Département]  ·  [Filière — ex. Génie Logiciel]", align="C")
    pdf.ln(6)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(80, pdf.get_y() + 2, 130, pdf.get_y() + 2)
    pdf.ln(12)
    pdf.image(os.path.join(FIGS, "fig01_logo.png"), x=85, w=40)
    pdf.ln(46)
    pdf.set_font("sans", "B", 13)
    pdf.set_text_color(*GOLD_DARK)
    pdf.cell(0, 7, "RAPPORT DE PROJET DE FIN D'ÉTUDES", align="C")
    pdf.ln(9)
    pdf.set_font("serif", "B", 19)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 9, "Conception et réalisation d'une\nplateforme e-commerce\npour la parapharmacie Cléopâtre", align="C")
    pdf.ln(3)
    pdf.set_font("sans", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 6, "Cléopâtre — Espace Santé Beauté  ·  Ezzahra – Hammam-Lif", align="C")
    pdf.ln(14)
    pdf.set_font("serif", "", 11)
    pdf.set_text_color(*INK)
    for label, val in [("Réalisé par :", "[Nom Prénom de l'étudiant(e)]"),
                       ("Encadrant académique :", "[Nom — Grade, Établissement]"),
                       ("Encadrant professionnel :", "[Nom — Responsable digital, Cléopâtre]")]:
        pdf.set_font("sans", "", 10)
        pdf.set_text_color(*MUTED)
        pdf.cell(62, 7, label, align="R")
        pdf.set_font("serif", "B", 11)
        pdf.set_text_color(*INK)
        pdf.cell(0, 7, "  " + val, align="L")
        pdf.ln(7)
    pdf.ln(8)
    pdf.set_font("sans", "", 10)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 6, "Année universitaire [20XX – 20XX]  ·  Soutenance du [JJ/MM/AAAA]", align="C")


def jury(pdf: Report):
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("sans", "B", 15)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, "Jury de soutenance", align="C")
    pdf.ln(10)
    pdf.set_font("serif", "", 11)
    pdf.set_text_color(*INK)
    pdf.cell(0, 7, "Ce travail a été présenté et soutenu publiquement le [JJ/MM/AAAA]", align="C")
    pdf.ln(7)
    pdf.cell(0, 7, "devant le jury composé de :", align="C")
    pdf.ln(12)
    # tableau jury via _table_inner
    pdf._table_inner(["Nom & Prénom", "Qualité", "Rôle dans le jury"],
                     [["[Nom Prénom]", "[Grade, Établissement]", "Président(e)"],
                      ["[Nom Prénom]", "[Grade, Établissement]", "Examinateur(trice)"],
                      ["[Nom Prénom]", "[Grade, Établissement]", "Encadrant académique"],
                      ["[Nom Prénom]", "[Fonction, Cléopâtre]", "Encadrant professionnel"]],
                     [52, 58, 56], 9.5)
    pdf.ln(6)
    pdf.set_font("serif", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 5.6, "La composition définitive du jury sera arrêtée par la direction des études. "
                           "Les noms, grades et qualités sont à compléter avant impression.", align="C")


def dedicaces(pdf: Report):
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("sans", "B", 15)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, "Dédicaces", align="C")
    pdf.ln(10)
    pdf.set_font("serif", "", 11)
    pdf.set_text_color(*INK)
    for t in ["À mes parents, pour leur amour inconditionnel, leurs sacrifices silencieux et leur confiance sans faille : ce diplôme est le leur avant d'être le mien.",
              "À mes frères et sœurs, pour leur soutien et leur bonne humeur qui ont adouci les longues soirées de code.",
              "À mes amis et camarades de promotion, compagnons de route de ces belles années d'études.",
              "À toute l'équipe de la parapharmacie Cléopâtre, pour son accueil chaleureux et sa confiance.",
              "Je dédie ce modeste travail à toutes celles et ceux qui croient que le travail sérieux finit toujours par payer."]:
        pdf.multi_cell(0, 6, t, align="J")
        pdf.ln(3)


def remerciements(pdf: Report):
    pdf.add_page()
    pdf.ln(6)
    pdf.set_font("sans", "B", 15)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, "Remerciements", align="C")
    pdf.ln(8)
    pdf.set_font("serif", "", 10.5)
    pdf.set_text_color(*INK)
    texts = [
        "Au terme de ce Projet de Fin d'Études, il m'est agréable d'adresser mes vifs remerciements à toutes les personnes qui ont contribué, de près ou de loin, à sa réalisation.",
        "J'exprime ma profonde gratitude à **M./Mme [Nom], mon encadrant académique**, pour sa disponibilité, ses conseils éclairés et son exigence méthodologique, qui ont structuré ce travail du cadrage Scrum jusqu'à la rédaction du présent rapport.",
        "Mes sincères remerciements vont à **M./Mme [Nom], Responsable digital de la parapharmacie Cléopâtre et encadrant professionnel**, pour la confiance témoignée en me confiant un projet réel et stratégique, pour sa vision produit qui a nourri chaque sprint, et pour le temps consacré aux revues et démonstrations.",
        "Je remercie chaleureusement **toute l'équipe de la maison Cléopâtre** — pharmaciens, vendeuses, préparateurs — pour leur accueil, leur patience face à mes questions et la richesse de leur connaissance métier, sans laquelle cette plateforme n'aurait ni âme ni pertinence.",
        "Je remercie les **membres du jury** d'avoir accepté d'évaluer ce travail, ainsi que **le corps enseignant de [Établissement]** pour la formation reçue tout au long de mon cursus.",
        "Enfin, merci à **ma famille et à mes proches**, dont le soutien constant a porté ce projet autant que le code.",
    ]
    for t in texts:
        pdf.multi_cell(0, 5.4, md(t), markdown=True, align="J")
        pdf.ln(2.2)


# ── sommaire & listes ────────────────────────────────────
def _dotted_entry(pdf, level, label, page, size=9.0, bold=False, link=""):
    lm, rm = pdf.l_margin, pdf.r_margin
    indent = level * 8
    pdf.set_font("sans" if bold else "serif", "B" if bold else "", size + (0.5 if bold else 0))
    pdf.set_text_color(*INK)
    pg = str(page)
    pg_w = pdf.get_string_width(pg) + 2
    avail = pdf.w - lm - rm - indent - pg_w - 4
    # tronquer si besoin
    while pdf.get_string_width(label) > avail and len(label) > 8:
        label = label[:-2]
    if pdf.get_string_width(label) > avail:
        label = label[: int(len(label) * avail / pdf.get_string_width(label)) - 1] + "…"
    x = lm + indent
    pdf.set_x(x)
    h = 5.4 if not bold else 6.0
    pdf.cell(pdf.get_string_width(label) + 1, h, label, link=link or "")
    x1 = pdf.get_x() + 1
    x2 = pdf.w - rm - pg_w
    dot_w = pdf.get_string_width(". ")
    n = max(0, int((x2 - x1) / dot_w))
    pdf.set_text_color(*MUTED)
    pdf.set_font("serif", "", size)
    pdf.cell(x2 - x1, h, ". " * n)
    pdf.set_text_color(*INK)
    pdf.set_font("sans" if bold else "serif", "B" if bold else "", size)
    pdf.cell(pg_w, h, pg, align="R", link=link or "")
    pdf.ln(h + (1.2 if bold else 0.4))


def toc_block(pdf, entries):
    pdf.current_chapter = "Table des matières"
    pdf.add_page()
    pdf.set_font("sans", "B", 15)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, "Table des matières", align="L")
    pdf.ln(8)
    for level, title, page, link in entries:
        if pdf.get_y() > 268:
            pdf.add_page()
        _dotted_entry(pdf, level, title, page, bold=(level == 0), link=link)


def list_block(pdf, title, entries, prefix, strip=""):
    pdf.current_chapter = title
    pdf.add_page()
    pdf.set_font("sans", "B", 15)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, title, align="L")
    pdf.ln(8)
    for num, caption, page, link in entries:
        if pdf.get_y() > 268:
            pdf.add_page()
        if strip and caption.startswith(strip):
            caption = caption[len(strip):]
        label = f"{prefix} {num} – {caption}"
        _dotted_entry(pdf, 0, label, page, size=8.6, link=link)


def abbr_block(pdf):
    pdf.current_chapter = "Liste des abréviations"
    pdf.add_page()
    pdf.set_font("sans", "B", 15)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, "Liste des abréviations", align="L")
    pdf.ln(8)
    pdf._table_inner(["Abréviation", "Signification"], ABBR, [34, 132], 9.2)


# ── rendu des blocs ─────────────────────────────────────
def render_block(pdf: Report, kind, payload):
    if kind == "h1":
        pdf.h1(payload)
    elif kind == "h2":
        pdf.h2(payload)
    elif kind == "h3":
        pdf.h3(payload)
    elif kind == "p":
        paragraph(pdf, payload)
    elif kind == "bullets":
        bullets(pdf, payload)
    elif kind == "enum":
        bullets(pdf, payload, numbered=True)
    elif kind == "table":
        caption, head, rows, widths = payload
        pdf.table_block(caption, head, rows, widths)
    elif kind == "figure":
        fname, caption = payload[0], payload[1]
        width = payload[2] if len(payload) > 2 else 150
        pdf.figure(os.path.join(FIGS, fname), caption, width)
    elif kind == "code":
        title, text = payload
        pdf.code_block(title, text)
    elif kind == "info":
        title, text = payload
        pdf.info_box(title, text)
    elif kind == "pagebreak":
        pdf.add_page()


def render_front_cover(pdf):
    cover(pdf)
    pdf.cover_done = True
    jury(pdf)
    dedicaces(pdf)
    remerciements(pdf)


def render_front_lists(pdf, toc, figs, tabs, codes):
    toc_block(pdf, toc)
    list_block(pdf, "Liste des figures", figs, "Figure")
    list_block(pdf, "Liste des tableaux", tabs, "Tableau")
    list_block(pdf, "Liste des extraits de code", codes, "Extrait", strip="Extrait — ")
    abbr_block(pdf)


BACK_INK = (43, 38, 32)
BACK_PAPER = (235, 228, 214)
BACK_MUT = (185, 172, 147)


def back_cover(pdf: Report):
    pdf.current_chapter = ""
    pdf.add_page()
    pdf.no_footer_pages.add(pdf.page_no())
    pdf.set_fill_color(*BACK_INK)
    pdf.rect(0, 0, 210, 297, style="F")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.7)
    pdf.rect(9, 9, 192, 279)
    pdf.set_line_width(0.25)
    pdf.rect(11.5, 11.5, 187, 274)
    pdf.set_xy(22, 30)
    pdf.set_font("sans", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 7, "RÉSUMÉ", align="C")
    pdf.ln(9)
    pdf.set_font("serif", "", 10)
    pdf.set_text_color(*BACK_PAPER)
    pdf.multi_cell(0, 5.4, "Ce rapport présente la conception et la réalisation d'une plateforme e-commerce "
        "complète pour la parapharmacie tunisienne Cléopâtre : site marchand (catalogue, recherche à "
        "facettes, tunnel de commande, suivi invité sécurisé) et back-office (commandes, stock, "
        "promotions, avis, support, audit). Conduite en Scrum (un sprint 0, quatre sprints en deux "
        "releases) et réalisée en Next.js, TypeScript et PostgreSQL, la plateforme applique des "
        "exigences fortes — montants en millimes, scrypt, sessions httpOnly, transactions verrouillées, "
        "commandes idempotentes — et reconstruit de zéro l'ancien site vitrine.", align="J")
    pdf.ln(3)
    pdf.set_font("serif", "B", 10)
    pdf.set_text_color(*BACK_MUT)
    pdf.multi_cell(0, 5.4, "Mots-clés : e-commerce, parapharmacie, Scrum, Next.js, PostgreSQL, UML, Docker.",
                   align="C")
    pdf.ln(8)
    pdf.set_font("sans", "B", 13)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 7, "ABSTRACT", align="C")
    pdf.ln(9)
    pdf.set_font("serif", "", 10)
    pdf.set_text_color(*BACK_PAPER)
    pdf.multi_cell(0, 5.4, "This report presents the design and implementation of a complete e-commerce "
        "platform for the Tunisian parapharmacy Cléopâtre: storefront (catalog, faceted search, checkout "
        "flow, secured guest tracking) and back-office (orders, inventory, promotions, reviews, support, "
        "audit). Conducted with Scrum (one sprint 0, four sprints in two releases) and built with "
        "Next.js, TypeScript and PostgreSQL, the platform enforces strong guarantees — integer millimes, "
        "scrypt, httpOnly sessions, locked transactions, idempotent orders — and rebuilds the legacy "
        "showcase site from scratch.", align="J")
    pdf.ln(3)
    pdf.set_font("serif", "B", 10)
    pdf.set_text_color(*BACK_MUT)
    pdf.multi_cell(0, 5.4, "Keywords: e-commerce, parapharmacy, Scrum, Next.js, PostgreSQL, UML, Docker.",
                   align="C")
    pdf.ln(14)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.6)
    pdf.line(80, pdf.get_y(), 130, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("sans", "", 10)
    pdf.set_text_color(*BACK_MUT)
    pdf.cell(0, 6, "[Établissement]  ·  [Diplôme — Filière]  ·  [20XX – 20XX]", align="C")


def render_body(pdf):
    for kind, payload in BODY:
        render_block(pdf, kind, payload)


def _mk_link(pdf, dest):
    lk = pdf.add_link()
    pdf.set_link(lk, page=dest[0], y=dest[1])
    return lk


def _with_links(pdf, entries, dests):
    assert len(entries) == len(dests), f"destinations désalignées: {len(entries)} != {len(dests)}"
    return [(a, b, c, _mk_link(pdf, d)) for (a, b, c, _), d in zip(entries, dests)]


def build():
    check_markup()
    # Passe 1 (mesure) : garde + corps + dos, pour relever les pages brutes
    m = Report()
    render_front_cover(m)
    f0 = m.page_no()
    render_body(m)
    back_cover(m)
    toc_raw = list(m.toc_entries)
    fig_raw = list(m.fig_entries)
    tab_raw = list(m.tab_entries)
    code_raw = list(m.code_entries)
    print(f"mesure: front_min={f0} pages, corps+dos={m.page_no() - f0} pages, "
          f"toc={len(toc_raw)}, fig={len(fig_raw)}, tab={len(tab_raw)}, code={len(code_raw)}")
    # Passe 2 (mesure du front complet, numéros factices)
    t = Report()
    render_front_cover(t)
    render_front_lists(t, [(l, ti, 1, "") for l, ti, _ in toc_raw],
                       [(n, c, 1, "") for n, c, _ in fig_raw],
                       [(n, c, 1, "") for n, c, _ in tab_raw],
                       [(n, c, 1, "") for n, c, _ in code_raw])
    F = t.page_no()
    shift = F - f0
    print(f"front complet={F} pages, décalage={shift}")
    toc = [(l, ti, p + shift, "") for l, ti, p in toc_raw]
    figs = [(n, c, p + shift, "") for n, c, p in fig_raw]
    tabs = [(n, c, p + shift, "") for n, c, p in tab_raw]
    codes = [(n, c, p + shift, "") for n, c, p in code_raw]
    # Passe 3 (destinations) : front réel sans liens + corps + dos
    r = Report()
    render_front_cover(r)
    render_front_lists(r, toc, figs, tabs, codes)
    assert r.page_no() == F, f"front instable p3: {r.page_no()} != {F}"
    render_body(r)
    back_cover(r)
    assert [p for _, _, p in r.toc_entries] == [p for _, _, p, _ in toc], "TOC instable p3"
    assert [p for _, _, p in r.fig_entries] == [p for _, _, p, _ in figs], "Fig instable p3"
    assert [p for _, _, p in r.tab_entries] == [p for _, _, p, _ in tabs], "Tab instable p3"
    assert [p for _, _, p in r.code_entries] == [p for _, _, p, _ in codes], "Code instable p3"
    # Passe 4 (finale) : front avec liens + corps + dos
    pdf = Report()
    pdf.set_title("Rapport PFE — Plateforme e-commerce pour la parapharmacie Cléopâtre")
    pdf.set_author("[Nom Prénom de l'étudiant(e)] — [Établissement]")
    pdf.set_subject("Projet de Fin d'Études — Scrum — Next.js / PostgreSQL")
    pdf.set_creator("build.py (fpdf2)")
    render_front_cover(pdf)
    render_front_lists(pdf, _with_links(pdf, toc, r.toc_dest),
                       _with_links(pdf, figs, r.fig_dest),
                       _with_links(pdf, tabs, r.tab_dest),
                       _with_links(pdf, codes, r.code_dest))
    assert pdf.page_no() == F, f"front instable: {pdf.page_no()} != {F}"
    render_body(pdf)
    back_cover(pdf)
    # vérification : les pages relevées doivent matcher
    assert [p for _, _, p in pdf.toc_entries] == [p for _, _, p, _ in toc], "TOC instable"
    assert [p for _, _, p in pdf.fig_entries] == [p for _, _, p, _ in figs], "Fig instable"
    assert [p for _, _, p in pdf.tab_entries] == [p for _, _, p, _ in tabs], "Tab instable"
    assert [p for _, _, p in pdf.code_entries] == [p for _, _, p, _ in codes], "Code instable"
    pdf.output(OUT_PDF)
    print(f"PDF généré : {OUT_PDF} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build()
