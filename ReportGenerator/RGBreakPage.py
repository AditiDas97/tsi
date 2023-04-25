try:
    from .RGHeadlines import mm, cm, A4, landscape
    from .RGPDF import PDF
except ImportError:
    from RGHeadlines import mm, cm, A4, landscape
    from RGPDF import PDF

class BreakPage:

    def __init__(self):
        self.page_break = "PageBreak"

    def to_text(self):
        return ""

    def to_json(self):
        return {"": ""}

    def to_html(self):
        return "<br></br>"

    def to_pdf(self, pdf):
        pdf.pdf.showPage()
        pdf.cursor.move(x=3 * cm, y=A4[1] - (2.9 * cm))


class ResizePage:

    def __init__(self, orientation='portrait'):
        self.orientation = orientation

    def to_text(self):
        return ""

    def to_json(self):
        return {"": ""}

    def to_pdf(self, pdf):
        if self.orientation == 'portrait':
            pdf.cursor.move(x=3 * cm, y=A4[1] - (2.9 * cm))
        else:
            pdf.cursor.move(x=3 * cm, y=landscape(A4)[1] - (2 * cm))
        pdf.set_page_size("A4", self.orientation)

    def to_html(self):
        return ""
