"""Moteur de génération du rapport PFE — briques de mise en page (fpdf2).

V14 « EDITORIAL REFORGE » : système éditorial extension du site —
Newsreader (titres, emphases) + Manrope (courant, données),
palette ivoire / encre profonde / champagne / sauge / terracotta contrôlé.
"""
from __future__ import annotations
import os
from fpdf import FPDF

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
NEWS_R = os.path.join(FONTS, "Newsreader-Regular.ttf")
NEWS_B = os.path.join(FONTS, "Newsreader-Bold.ttf")
NEWS_I = os.path.join(FONTS, "Newsreader-Italic.ttf")
NEWS_BI = os.path.join(FONTS, "Newsreader-BoldItalic.ttf")
MAN_R = os.path.join(FONTS, "Manrope-Regular.ttf")
MAN_B = os.path.join(FONTS, "Manrope-Bold.ttf")
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

INK = (31, 27, 22)
MUTED = (122, 112, 98)
GOLD = (201, 169, 89)
GOLD_DARK = (140, 105, 36)
IVORY = (245, 239, 227)
STONE_LINE = (214, 203, 184)
SHADE = (245, 239, 227)
SHADE2 = (238, 231, 216)
CODE_BG = (243, 240, 233)
WHITE = (255, 255, 255)
SAGE = (125, 140, 111)
SAGE_D = (93, 110, 82)
SAGE_L = (233, 237, 226)
TERRA = (176, 97, 63)
TERRA_L = (243, 228, 219)


class Report(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(22, 20, 22)
        self.set_auto_page_break(True, margin=20)
        self.add_font("serif", "", NEWS_R)
        self.add_font("serif", "B", NEWS_B)
        self.add_font("serif", "I", NEWS_I)
        self.add_font("serif", "BI", NEWS_BI)
        self.add_font("sans", "", MAN_R)
        self.add_font("sans", "B", MAN_B)
        self.add_font("mono", "", MONO)
        self.add_font("mono", "B", MONO_B)
        # state
        self.fig_no = 0
        self.tab_no = 0
        self.code_no = 0
        self.toc_entries: list[tuple[int, str, int]] = []
        self.fig_entries: list[tuple[int, str, int]] = []
        self.tab_entries: list[tuple[int, str, int]] = []
        self.code_entries: list[tuple[int, str, int]] = []
        self.toc_dest: list[tuple[int, float]] = []
        self.fig_dest: list[tuple[int, float]] = []
        self.tab_dest: list[tuple[int, float]] = []
        self.code_dest: list[tuple[int, float]] = []
        self.current_chapter = ""
        self.show_footer = True
        self.cover_done = False
        self.no_footer_pages: set[int] = set()

    # ── header / footer ──────────────────────────────────
    def header(self):
        if self.page_no() == 1 or not self.cover_done:
            return
        if self.current_chapter:
            self.set_font("sans", "", 7)
            self.set_text_color(*MUTED)
            self.cell(0, 6, self.current_chapter.upper(), align="R")
            self.set_draw_color(*STONE_LINE)
            self.set_line_width(0.2)
            self.line(self.l_margin, 15.5, self.w - self.r_margin, 15.5)
            self.ln(9)

    def footer(self):
        if self.page_no() == 1 or not self.show_footer or self.page_no() in self.no_footer_pages:
            return
        self.set_y(-14)
        self.set_draw_color(*STONE_LINE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_font("sans", "B", 8.5)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 7, f"— {self.page_no()} —", align="C")

    # ── titres ───────────────────────────────────────────
    def h1(self, payload, toc=True):
        """Intercalaire éditorial (tuple) ou tête de section directe (str)."""
        if isinstance(payload, str):
            self._h1_direct(payload, toc)
        else:
            title, eyebrow, epigraph, short = payload
            self._h1_divider(title, eyebrow, epigraph, short, toc)

    def _h1_direct(self, text, toc=True):
        self.current_chapter = text
        self.add_page()
        if toc:
            self.start_section(text, level=0)
            self.toc_entries.append((0, text, self.page_no()))
            self.toc_dest.append((self.page_no(), self.get_y()))
        self.ln(4)
        W = self.w - self.l_margin - self.r_margin
        self.set_font("serif", "B", 18)
        self.set_text_color(*INK)
        self.multi_cell(W, 9, text, align="L")
        self.set_draw_color(*GOLD)
        self.set_line_width(1.0)
        self.line(self.l_margin, self.get_y() + 3, self.l_margin + 34, self.get_y() + 3)
        self.ln(10)

    def _h1_divider(self, title, eyebrow, epigraph, short, toc=True):
        self.current_chapter = ""
        self.add_page()
        self.no_footer_pages.add(self.page_no())
        if toc:
            self.start_section(title, level=0)
            self.toc_entries.append((0, title, self.page_no()))
            self.toc_dest.append((self.page_no(), self.get_y()))
        W = self.w - self.l_margin - self.r_margin
        self.set_y(72)
        # eyebrow
        self.set_font("sans", "B", 10)
        self.set_text_color(*GOLD_DARK)
        self.multi_cell(0, 6, eyebrow.upper(), align="C")
        self.ln(4)
        # title
        self.set_font("serif", "B", 30)
        self.set_text_color(*INK)
        self.multi_cell(0, 13.5, title, align="C")
        self.ln(6)
        # champagne double rule
        cx = self.w / 2
        y = self.get_y()
        self.set_draw_color(*GOLD)
        self.set_line_width(1.0)
        self.line(cx - 30, y, cx + 30, y)
        self.set_line_width(0.3)
        self.line(cx - 30, y + 2.4, cx + 30, y + 2.4)
        self.ln(10)
        # epigraph
        self.set_font("serif", "I", 11)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 6.2, epigraph, align="C")
        # bottom ornament: small diamond + part label
        self.set_y(248)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        y0 = self.get_y()
        self.line(cx - 34, y0, cx - 8, y0)
        self.line(cx + 8, y0, cx + 34, y0)
        self.set_fill_color(*GOLD)
        self.polygon([(cx, y0 - 3.2), (cx + 3.2, y0), (cx, y0 + 3.2), (cx - 3.2, y0)], style="F")
        self.set_xy(self.l_margin, y0 + 6)
        self.set_font("sans", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 5, short.upper(), align="C")
        self.ln(5)
        # l'intercalaire occupe sa page seul : le corps commence en page fraîche
        self.current_chapter = short
        self.add_page()

    def h2(self, text, toc=True):
        if self.get_y() > 238:
            self.add_page()
        if toc:
            self.start_section(text, level=1)
            self.toc_entries.append((1, text, self.page_no()))
            self.toc_dest.append((self.page_no(), self.get_y()))
        self.ln(4)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.9)
        self.line(self.l_margin, self.get_y(), self.l_margin + 14, self.get_y())
        self.ln(3)
        self.set_font("sans", "B", 12.5)
        self.set_text_color(*INK)
        self.multi_cell(0, 6.6, text)
        self.ln(2)

    def h3(self, text, toc=True):
        if self.get_y() > 252:
            self.add_page()
        if toc:
            self.start_section(text, level=2)
            self.toc_entries.append((2, text, self.page_no()))
            self.toc_dest.append((self.page_no(), self.get_y()))
        self.ln(2.5)
        self.set_font("sans", "B", 10.5)
        self.set_text_color(*GOLD_DARK)
        self.multi_cell(0, 5.8, text)
        self.ln(1.5)

    def transition(self, text):
        if self.get_y() > 250:
            self.add_page()
        self.ln(4)
        W = self.w - self.l_margin - self.r_margin
        y = self.get_y()
        self.set_draw_color(*GOLD)
        self.set_line_width(0.4)
        self.line(self.l_margin + 18, y + 3, self.l_margin + 44, y + 3)
        self.line(self.w - self.r_margin - 44, y + 3, self.w - self.r_margin - 18, y + 3)
        self.set_font("serif", "I", 10.5)
        self.set_text_color(*MUTED)
        self.set_x(self.l_margin + 48)
        self.multi_cell(W - 96, 5.6, text, align="C")
        self.ln(6)

    # ── tableaux ─────────────────────────────────────────
    def table_block(self, caption, head, rows, widths=None, size=8.6):
        self.tab_no += 1
        if self.get_y() + 6 > self.page_break_trigger:
            self.add_page()
        self.tab_dest.append((self.page_no(), self.get_y()))
        self._table_inner(head, rows, widths, size)
        self.set_font("sans", "B", 7.5)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 4.6, f"TABLEAU {self.tab_no}", align="C")
        self.ln(4.6)
        self.set_font("sans", "", 8.5)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 4.4, caption, align="C")
        self.tab_entries.append((self.tab_no, caption, self.page_no()))
        self.ln(4)

    def _cell_lines(self, text, width, family, style, size):
        self.set_font(family, style, size)
        lines = self.multi_cell(width - 2, 5.0, str(text), dry_run=True, output="LINES")
        return max(1, len(lines))

    def _table_inner(self, head, rows, widths=None, size=8.6):
        W = self.w - self.l_margin - self.r_margin
        n = len(head)
        if widths is None:
            widths = [W / n] * n
        else:
            s = sum(widths)
            widths = [w / s * W for w in widths]
        lh = 5.0
        hh = max(self._cell_lines(h, widths[i], "sans", "B", size) for i, h in enumerate(head)) * lh
        if self.get_y() + hh > self.page_break_trigger:
            self.add_page()
        y0 = self.get_y()
        self.set_fill_color(*INK)
        self.rect(self.l_margin, y0, W, hh, style="F")
        self.set_text_color(*WHITE)
        x = self.l_margin
        for i, h in enumerate(head):
            self.set_xy(x + 1, y0)
            self.set_font("sans", "B", size)
            self.multi_cell(widths[i] - 2, lh, h, border=0, align="C")
            x += widths[i]
        self.set_draw_color(120, 112, 100)
        self.set_line_width(0.2)
        xx = self.l_margin
        for i in range(n - 1):
            xx += widths[i]
            self.line(xx, y0, xx, y0 + hh)
        self.set_draw_color(*INK)
        self.set_line_width(0.3)
        self.rect(self.l_margin, y0, W, hh, style="D")
        self.set_y(y0 + hh)
        for ri, row in enumerate(rows):
            row = [str(c) for c in row]
            rh = max(self._cell_lines(c, widths[i], "sans", "B" if i == 0 else "", size)
                     for i, c in enumerate(row)) * lh
            if self.get_y() + rh > self.page_break_trigger:
                self.add_page()
            y0 = self.get_y()
            if ri % 2 == 1:
                self.set_fill_color(*IVORY)
                self.rect(self.l_margin, y0, W, rh, style="F")
            x = self.l_margin
            for i, c in enumerate(row):
                self.set_xy(x + 1, y0)
                self.set_font("sans", "B" if i == 0 else "", size)
                self.set_text_color(*INK)
                self.multi_cell(widths[i] - 2, lh, c, border=0, align="L")
                x += widths[i]
            self.set_draw_color(*STONE_LINE)
            self.set_line_width(0.2)
            self.rect(self.l_margin, y0, W, rh, style="D")
            xx = self.l_margin
            for i in range(n - 1):
                xx += widths[i]
                self.line(xx, y0, xx, y0 + rh)
        self.ln(2)

    def plain_table(self, head, rows, widths=None, size=8.6):
        self._table_inner(head, rows, widths, size)
        self.ln(2)

    # ── figures ──────────────────────────────────────────
    def figure(self, path, title, width=150, baseline=None, source=None):
        import os as _os
        if not _os.path.exists(path):
            self.capture("FIGURE", title,
                         f"Fichier { _os.path.basename(path)} — à générer", width=width)
            return
        self.fig_no += 1
        from PIL import Image as PILImage
        try:
            im = PILImage.open(path)
            ratio = im.height / im.width
            est = width * ratio + 22
        except Exception:
            est = 80
        if self.get_y() + min(est, 120) > self.page_break_trigger and self.get_y() > 60:
            self.add_page()
        self.fig_dest.append((self.page_no(), self.get_y()))
        x = (self.w - width) / 2
        self.image(path, x=x, w=width)
        self.ln(2.5)
        self.set_font("sans", "B", 7.5)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 4.4, f"FIGURE {self.fig_no}", align="C")
        self.ln(4.4)
        self.set_font("sans", "B", 9)
        self.set_text_color(*INK)
        self.multi_cell(0, 4.6, title, align="C")
        self.set_x(self.l_margin)
        if baseline:
            self.set_font("sans", "", 8)
            self.set_text_color(*MUTED)
            self.multi_cell(0, 4.2, baseline, align="C")
            self.set_x(self.l_margin)
        if source:
            self.set_font("sans", "", 7)
            self.set_text_color(*MUTED)
            self.multi_cell(0, 4.0, f"Source : {source}", align="C")
        entry = title if not baseline else f"{title} — {baseline}"
        self.fig_entries.append((self.fig_no, entry, self.page_no()))
        self.ln(4)

    # ── bloc preuve ──────────────────────────────────────
    def proof(self, number, text, source):
        W = self.w - self.l_margin - self.r_margin
        n = self._cell_lines(text, W - 34, "sans", "", 9.5)
        bh = max(24, n * 5.2 + 14)
        if self.get_y() + bh > self.page_break_trigger:
            self.add_page()
        y0 = self.get_y()
        x = self.l_margin
        self.set_fill_color(*IVORY)
        self.set_draw_color(*STONE_LINE)
        self.set_line_width(0.3)
        self.rect(x, y0, W, bh, style="DF")
        self.set_fill_color(*GOLD)
        self.rect(x, y0, 2.2, bh, style="F")
        self.set_xy(x + 6, y0 + 3)
        self.set_font("serif", "B", 21)
        self.set_text_color(*GOLD_DARK)
        self.cell(20, 12, number)
        self.set_xy(x + 28, y0 + 3.5)
        self.set_font("sans", "", 9.5)
        self.set_text_color(*INK)
        self.multi_cell(W - 32, 5.2, text)
        self.set_x(x + 28)
        self.set_font("sans", "B", 7)
        self.set_text_color(*MUTED)
        self.cell(W - 32, 4.2, f"SOURCE : {source}")
        self.set_y(y0 + bh + 4)

    # ── emplacement de capture (AVANT / APRÈS) ────────────
    def capture(self, kind, label, note, width=166):
        """Cadre 16:9 élégant. kind ∈ {AVANT, APRÈS, FIGURE}."""
        colors = {"AVANT": TERRA, "APRÈS": SAGE_D, "FIGURE": GOLD_DARK}
        fills = {"AVANT": TERRA_L, "APRÈS": SAGE_L, "FIGURE": IVORY}
        col = colors.get(kind, GOLD_DARK)
        h = width * 9 / 16
        need = h + 26
        if self.get_y() + need > self.page_break_trigger and self.get_y() > 60:
            self.add_page()
        self.fig_no += 1
        self.fig_dest.append((self.page_no(), self.get_y()))
        x = (self.w - width) / 2
        y0 = self.get_y()
        self.set_fill_color(*fills.get(kind, IVORY))
        self.set_draw_color(*col)
        self.set_line_width(0.5)
        try:
            self.set_dash_pattern(dash=3, gap=2.2)
        except Exception:
            pass
        self.rect(x, y0, width, h, style="DF")
        try:
            self.set_dash_pattern()
        except Exception:
            pass
        # badge
        bw = 30
        self.set_fill_color(*col)
        self.rect(x + width / 2 - bw / 2, y0 + h / 2 - 20, bw, 8, style="F")
        self.set_xy(x + width / 2 - bw / 2, y0 + h / 2 - 20)
        self.set_font("sans", "B", 8)
        self.set_text_color(*WHITE)
        self.cell(bw, 8, kind, align="C")
        self.set_xy(x, y0 + h / 2 - 9)
        self.set_font("serif", "B", 12)
        self.set_text_color(*INK)
        self.multi_cell(width, 6, label, align="C")
        self.set_x(x)
        self.set_font("sans", "B", 8.5)
        self.set_text_color(*col)
        self.cell(width, 5.5, "[CAPTURE À INSÉRER — FORMAT 16:9]", align="C")
        self.ln(5.5)
        self.set_x(x)
        self.set_font("sans", "", 7.5)
        self.set_text_color(*MUTED)
        self.multi_cell(width, 4.2, note, align="C")
        self.set_y(y0 + h + 3)
        self.set_x(self.l_margin)
        self.set_font("sans", "B", 7.5)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 4.4, f"FIGURE {self.fig_no}", align="C")
        self.ln(4.4)
        self.set_font("sans", "B", 9)
        self.set_text_color(*INK)
        self.multi_cell(0, 4.6, f"{kind} — {label} (emplacement réservé)", align="C")
        self.set_x(self.l_margin)
        self.fig_entries.append((self.fig_no, f"{kind} — {label} (emplacement réservé)",
                                 self.page_no()))
        self.ln(4)

    # ── code ─────────────────────────────────────────────
    def code_block(self, title, text, size=8.0):
        if self.get_y() > 235:
            self.add_page()
        self.code_no += 1
        self.code_dest.append((self.page_no(), self.get_y()))
        self.set_font("sans", "B", 8.5)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 5, title, align="L")
        self.ln(5.5)
        y0 = self.get_y()
        self.set_fill_color(*CODE_BG)
        self.set_font("mono", "", size)
        self.set_text_color(*INK)
        x = self.l_margin
        W = self.w - self.l_margin - self.r_margin
        for line in text.split("\n"):
            if self.get_y() + 4.6 > self.page_break_trigger:
                self.add_page()
            self.set_x(x)
            self.cell(W, 4.4, "  " + line.replace("\t", "  ")[:120], fill=True)
            self.ln(4.4)
        y1 = self.get_y()
        self.set_fill_color(*GOLD)
        # barreau champagne sur la première page du bloc
        self.code_entries.append((self.code_no, title, self.page_no()))
        self.ln(4)

    def info_box(self, title, text):
        if self.get_y() + 30 > self.page_break_trigger:
            self.add_page()
        x = self.l_margin
        W = self.w - self.l_margin - self.r_margin
        y0 = self.get_y()
        self.set_xy(x + 6, y0 + 3)
        self.set_font("sans", "B", 9.5)
        self.set_text_color(*GOLD_DARK)
        self.multi_cell(W - 12, 5, title)
        self.set_x(x + 6)
        self.set_font("sans", "", 9.5)
        self.set_text_color(*INK)
        self.multi_cell(W - 12, 5, text)
        y1 = self.get_y() + 3
        self.set_fill_color(*IVORY)
        self.set_draw_color(*STONE_LINE)
        self.set_line_width(0.3)
        # fond + cadre (redessinés autour du texte mesuré)
        self.ln(1)
        self.set_y(y1 + 3)
