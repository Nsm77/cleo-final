"""Moteur de génération du rapport PFE — briques de mise en page (fpdf2)."""
from __future__ import annotations
import os
import re
from fpdf import FPDF

FONTS = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONTS, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONTS, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONTS, "DejaVuSans.ttf")
SANS_B = os.path.join(FONTS, "DejaVuSans-Bold.ttf")
MONO = os.path.join(FONTS, "DejaVuSansMono.ttf")
MONO_B = os.path.join(FONTS, "DejaVuSansMono-Bold.ttf")

INK = (43, 38, 32)
MUTED = (112, 104, 92)
GOLD = (140, 105, 36)
GOLD_DARK = (110, 82, 26)
STONE_LINE = (208, 198, 182)
SHADE = (247, 243, 235)
SHADE2 = (240, 234, 223)
CODE_BG = (243, 240, 234)
WHITE = (255, 255, 255)


class Report(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(22, 20, 22)
        self.set_auto_page_break(True, margin=20)
        self.add_font("serif", "", SERIF)
        self.add_font("serif", "B", SERIF_B)
        self.add_font("sans", "", SANS)
        self.add_font("sans", "B", SANS_B)
        self.add_font("mono", "", MONO)
        self.add_font("mono", "B", MONO_B)
        # state
        self.fig_no = 0
        self.tab_no = 0
        self.toc_entries: list[tuple[int, str, int]] = []
        self.fig_entries: list[tuple[int, str, int]] = []
        self.tab_entries: list[tuple[int, str, int]] = []
        self.current_chapter = ""
        self.show_footer = True
        self.cover_done = False

    # ── header / footer ──────────────────────────────────
    def header(self):
        if self.page_no() == 1 or not self.cover_done:
            return
        if self.current_chapter:
            self.set_font("sans", "", 7.5)
            self.set_text_color(*MUTED)
            self.cell(0, 6, self.current_chapter, align="R")
            self.set_draw_color(*STONE_LINE)
            self.set_line_width(0.2)
            self.line(self.l_margin, 15.5, self.w - self.r_margin, 15.5)
            self.ln(9)

    def footer(self):
        if self.page_no() == 1 or not self.show_footer:
            return
        self.set_y(-14)
        self.set_draw_color(*STONE_LINE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_font("sans", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 7, f"{self.page_no()}", align="C")

    # ── inline markup : **gras** et `code` ───────────────
    def rich_line(self, text: str, base_family="serif", base_size=10.5, align="J"):
        parts = re.split(r"(\*\*.+?\*\*|`.+?`)", text)
        x0 = self.get_x()
        w = self.w - self.l_margin - self.r_margin
        self.set_text_color(*INK)
        for part in parts:
            if not part:
                continue
            if part.startswith("**") and part.endswith("**"):
                self.set_font(base_family, "B", base_size)
                self.write(5.2, part[2:-2])
            elif part.startswith("`") and part.endswith("`"):
                self.set_font("mono", "", base_size - 1.2)
                self.write(5.2, part[1:-1])
            else:
                self.set_font(base_family, "", base_size)
                self.write(5.2, part)
        self.ln(5.6)

    def paragraph(self, text: str, size=10.5):
        for para in text.split("\n"):
            if para.strip() == "":
                self.ln(2.5)
                continue
            self.rich_line(para.strip(), size=size)
        self.ln(1.2)

    def bullets(self, items, size=10.5, numbered=False):
        for i, it in enumerate(items, 1):
            x = self.l_margin
            self.set_x(x)
            self.set_font("sans", "B", size)
            self.set_text_color(*GOLD_DARK)
            bullet = f"{i}." if numbered else "•"
            self.cell(7, 5.4, bullet)
            x1 = self.get_x()
            self.set_text_color(*INK)
            # render item with inline markup in remaining width
            parts = re.split(r"(\*\*.+?\*\*|`.+?`)", it)
            for part in parts:
                if not part:
                    continue
                if part.startswith("**") and part.endswith("**"):
                    self.set_font("serif", "B", size)
                    self.write(5.4, part[2:-2])
                elif part.startswith("`") and part.endswith("`"):
                    self.set_font("mono", "", size - 1.2)
                    self.write(5.4, part[1:-1])
                else:
                    self.set_font("serif", "", size)
                    self.write(5.4, part)
            self.ln(5.8)
        self.ln(1.5)

    # ── titres ───────────────────────────────────────────
    def h1(self, text, toc=True, break_before=True):
        self.current_chapter = text
        if break_before:
            self.add_page()
        if toc:
            self.start_section(text, level=0)
            self.toc_entries.append((0, text, self.page_no()))
        self.ln(6)
        self.set_font("sans", "B", 21)
        self.set_text_color(*INK)
        # small gold rule
        self.set_draw_color(*GOLD)
        self.set_line_width(1.1)
        self.multi_cell(0, 10, text, align="L")
        y = self.get_y()
        self.line(self.l_margin, y + 1, self.l_margin + 34, y + 1)
        self.ln(9)

    def h2(self, text, toc=True):
        if self.get_y() > 240:
            self.add_page()
        if toc:
            self.start_section(text, level=1)
            self.toc_entries.append((1, text, self.page_no()))
        self.ln(3)
        self.set_font("sans", "B", 13.5)
        self.set_text_color(*GOLD_DARK)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def h3(self, text, toc=True):
        if self.get_y() > 252:
            self.add_page()
        if toc:
            self.start_section(text, level=2)
            self.toc_entries.append((2, text, self.page_no()))
        self.ln(2)
        self.set_font("sans", "B", 11)
        self.set_text_color(*INK)
        self.multi_cell(0, 6, text)
        self.ln(1.5)

    # ── tableaux ─────────────────────────────────────────
    def table_block(self, caption, head, rows, widths=None, size=8.6):
        self.tab_no += 1
        self._table_inner(head, rows, widths, size)
        self.set_font("sans", "", 8.5)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 4.6, f"Tableau {self.tab_no} – {caption}", align="C")
        self.tab_entries.append((self.tab_no, caption, self.page_no()))
        self.ln(4)

    def _cell_lines(self, text, width, family, style, size):
        # mesure exacte via le moteur de césure de fpdf2 (rendu à blanc)
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
        # ── en-tête : fond plein + grille manuelle ──
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
        # séparateurs verticaux clairs
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
        # ── lignes : fond + texte + grille manuelle ──
        for ri, row in enumerate(rows):
            row = [str(c) for c in row]
            rh = max(self._cell_lines(c, widths[i], "serif", "B" if i == 0 else "", size)
                     for i, c in enumerate(row)) * lh
            if self.get_y() + rh > self.page_break_trigger:
                self.add_page()
            y0 = self.get_y()
            if ri % 2 == 1:
                self.set_fill_color(*SHADE)
                self.rect(self.l_margin, y0, W, rh, style="F")
            x = self.l_margin
            for i, c in enumerate(row):
                self.set_xy(x + 1, y0)
                self.set_font("serif", "B" if i == 0 else "", size)
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
    def figure(self, path, caption, width=150):
        self.fig_no += 1
        # estimate height to avoid orphan caption
        from PIL import Image as PILImage
        try:
            im = PILImage.open(path)
            ratio = im.height / im.width
            est = width * ratio + 14
        except Exception:
            est = 80
        if self.get_y() + min(est, 120) > self.page_break_trigger and self.get_y() > 60:
            self.add_page()
        x = (self.w - width) / 2
        self.image(path, x=x, w=width)
        self.ln(2)
        self.set_font("sans", "", 8.5)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 4.6, f"Figure {self.fig_no} – {caption}", align="C")
        self.fig_entries.append((self.fig_no, caption, self.page_no()))
        self.ln(4)

    def code_block(self, title, text, size=8.0):
        if self.get_y() > 235:
            self.add_page()
        self.set_font("sans", "B", 8.5)
        self.set_text_color(*GOLD_DARK)
        self.cell(0, 5, title, align="L")
        self.ln(5.5)
        self.set_fill_color(*CODE_BG)
        self.set_draw_color(*STONE_LINE)
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
        self.ln(4)

    def info_box(self, title, text):
        if self.get_y() + 30 > self.page_break_trigger:
            self.add_page()
        self.set_fill_color(*SHADE)
        self.set_draw_color(*GOLD)
        x = self.l_margin
        W = self.w - self.l_margin - self.r_margin
        y0 = self.get_y()
        self.set_xy(x + 4, y0 + 3)
        self.set_font("sans", "B", 9.5)
        self.set_text_color(*GOLD_DARK)
        self.multi_cell(W - 8, 5, title)
        self.set_x(x + 4)
        self.set_font("serif", "", 9.5)
        self.set_text_color(*INK)
        self.multi_cell(W - 8, 5, text)
        y1 = self.get_y() + 3
        # redraw frame behind? draw rect outline
        self.set_line_width(0.4)
        self.rect(x, y0, W, y1 - y0)
        self.set_xy(x, y1 + 3)
        # fill behind text: paint first then text — simpler: keep white + border
        self.ln(1)
