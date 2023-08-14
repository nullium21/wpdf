from dataclasses import dataclass

from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.outline import OutlineSection
from fpdf.fpdf import ToCPlaceholder
from fpdf.syntax import DestinationXYZ


@dataclass
class FontSet:
    regular: str
    bold: str
    italic: str


class Document(FPDF):
    def __init__(self, fonts: FontSet, default_size: int = 12):
        super().__init__("portrait", "mm", "A4")
        self.set_fonts(fonts, default_size)

    def set_fonts(self, fonts: FontSet, default_size: int):
        self.add_font(family='default', fname=fonts.regular)
        self.add_font(family='default', style='B', fname=fonts.bold)
        self.add_font(family='default', style='I', fname=fonts.italic)
        self.set_font('default', size=default_size)

    @property
    def _full_width(self):
        return self.epw + self.l_margin + self.r_margin

    @property
    def _full_height(self):
        return self.eph + self.t_margin + self.b_margin

    def add_cover(self, cover_url: str):
        self.add_page()
        self.image(cover_url, x=0, y=0, w=self._full_width, h=self._full_height)

    @staticmethod
    def _render_toc(self: "Document", outline: list[OutlineSection]):
        for section in outline:
            dest: DestinationXYZ = section.dest

            link = self.add_link(dest.top, dest.left, dest.page_number, dest.zoom)
            self.cell(0, txt=section.name, align='L', link=link, new_x='LMARGIN')
            self.cell(0, txt=str(section.page_number), align='R', link=link, new_x='LMARGIN', new_y='NEXT')

        # if our ToC is too small, pad it with pages.
        expected_final_page = self._toc_placeholder.start_page + self._toc_placeholder.pages - 1
        for _ in range(self.page, expected_final_page):
            self.add_page()

    def add_toc_page(self, title: str, n_pages: int = 2):
        self.add_page()
        self.start_section('Table of Contents', level=1)

        with self.use_font_face(FontFace(emphasis="BOLD", size_pt=18)):
            self.cell(txt=title, new_x='LMARGIN', new_y='NEXT', center=True)

        with self.use_font_face(FontFace(size_pt=16)):
            self.cell(h=20, txt='Table of Contents', new_x='LMARGIN', new_y='NEXT', center=True)

        self._toc_placeholder = ToCPlaceholder(self._render_toc, self.page, self.y, n_pages)
        for _ in range(1, self._toc_placeholder.pages):
            self.add_page()

    def add_chapter(self, title: str, content: str):
        self.add_page()
        self.start_section(title, level=1)

        with self.use_font_face(FontFace(emphasis="BOLD", size_pt=16)):
            self.cell(txt=title, new_x='LMARGIN', new_y='NEXT', center=True)
        self.write_html(content)
