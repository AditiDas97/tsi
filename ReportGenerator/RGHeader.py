try:
    from .RGHeadlines import mm, cm, A4, landscape, math, re, sort_col, ParagraphStyle, Paragraph
    from .RGStyle import RGStyle
    from .RGPDF import PDF
except ImportError:
    from RGHeadlines import mm, cm, A4, landscape, math, re, sort_col, ParagraphStyle, Paragraph
    from RGStyle import RGStyle
    from RGPDF import PDF


class RGHeader:

    def __init__(self, value=str("Temp"), level=int(1), style=RGStyle(), table=0):
        if value == '':
            value = " "
        self.content = value
        self.level = level
        self.header_style = style
        self.header_style.margin_left += ((self.level * 1 * cm) / 4)
        self.header_style.update_style()
        self.table = table

    def to_text(self):
        return self.content + "\n"

    def to_json(self):
        return {'level': self.level, 'text': self.content, 'type': 'Header', 'id': self.header_style.id,
                'fontSize': self.header_style.font_size, 'fontName': self.header_style.font_family,
                'textColor': self.header_style.color, 'marginRight': self.header_style.margin_right,
                'marginLeft': self.header_style.margin_left, 'marginBottom': self.header_style.margin_bottom,
                'marginTop': self.header_style.margin_top, 'backColor': self.header_style.bgcolor,
                'align': self.header_style.align, 'table': self.table}

    def to_pdf(self, pdf):

        line_tag = self.content
        link = re.findall(r'(<a.*?</a>)', line_tag)
        content_end = list()
        content_p = re.split(r'(<a.*?</a>)', line_tag)
        temp_text = str()
        for k in content_p:
            if k.find("<a") >= 0 or k.find("</a>") >= 0:
                pass
            elif k != '':
                content_end.append(k)
        if len(link) <= 0:
            temp_text = line_tag
        else:
            result_href = list()
            for j in link:
                tmp = re.findall(r'=.*?>', j)
                tmp2 = re.split(r'[=>]', tmp[0])
                result_href.append(tmp2[1])
            temp_result = re.findall(r'(>.*?</a>)', line_tag)
            result_text = list()
            for j in temp_result:
                tmp = re.findall(r'[A-Za-z0-9].*[^</a>]', j)
                result_text.append(tmp[0])
            list_end = list()
            for k in content_end:
                list_end.append([k, line_tag.find(k), "text"])
            for k in range(len(result_text)):
                list_end.append(
                    [result_text[k], line_tag.find(result_text[k]), "href", result_href[k]])
            list_end.sort(key=sort_col)


        temp_content = '<a name="%s"/>' %self.header_style.id + self.content

        if self.header_style.align == 'center':
            if len(link) <= 0:
                pdf.set_position_cursor((pdf.pdf._pagesize[0] / 2) + self.header_style.margin_left -
                                        ((math.ceil(self.header_style.font_size / 1.6666667) * len(self.content)) / 2),
                                        pdf.cursor.get_y() - self.header_style.margin_top)
            else:
                pdf.set_position_cursor((pdf.pdf._pagesize[0] / 2) -
                                        ((math.ceil(self.header_style.font_size / 1.6666667) * len(max(result_text))) / 2) +
					self.header_style.margin_left, pdf.cursor.get_y() - self.header_style.margin_top)
        elif self.header_style.align == 'left':
            pdf.set_position_cursor(3 * cm - self.header_style.margin_left, pdf.cursor.get_y())
        elif self.header_style.align == 'right':
            if len(link) <= 0:
                pdf.set_position_cursor(pdf.pdf._pagesize[0] - (math.ceil(self.header_style.font_size / 1.6666667) * len(
                    self.content)) - 1.5 * cm - self.header_style.margin_right, pdf.cursor.get_y())
            else:
                pdf.set_position_cursor(pdf.pdf._pagesize[0] - (math.ceil(self.header_style.font_size / 1.6666667) * len(
                    max(result_text))) - 1.5 * cm - self.header_style.margin_right, pdf.cursor.get_y())

        temp_font_name = 'Courier'
        if self.header_style.font_family == 'Courier new':
            temp_font_name = 'Courier'
        elif self.header_style.font_family == 'Arial':
            temp_font_name = 'Helvetica'
        elif self.header_style.font_family == 'Times' or self.header_style.font_family == 'Times New Roman':
            temp_font_name = 'Times-Roman'
        paragrahp_style = ParagraphStyle(name=self.header_style.id, fontSize=self.header_style.font_size,
                                         fontName=temp_font_name,
                                         textColor=self.header_style.color)
        textobject = pdf.pdf.beginText()

        text = Paragraph(temp_content, paragrahp_style)

        if self.header_style.bgcolor != "white" or self.header_style.bgcolor != "White":
            pdf.pdf.setFillColor(self.header_style.bgcolor)
            pdf.pdf.setStrokeColor(self.header_style.bgcolor)
            if pdf.pdf._pagesize == A4:
                pdf.pdf.rect(3 * cm,
                             pdf.cursor.get_y() - self.header_style.font_size / 3 - self.header_style.margin_top,
                             A4[0] - 3 * cm - 1.5 * cm, self.header_style.font_size, fill=1)
            elif pdf.pdf._pagesize == landscape(A4):
                pdf.pdf.rect(3 * cm,
                             pdf.cursor.get_y() - self.header_style.font_size / 3 - self.header_style.margin_top,
                             landscape(A4)[0] - 3 * cm - 1.5 * cm,
                             self.header_style.font_size, fill=1)

        temp_vector = []
        if math.ceil(self.header_style.font_size / 1.6666667) * len(self.content) > (pdf.pdf._pagesize[0] - 2 * cm
                                                                                     - 1.5 - cm):
            temp_str = self.content
            for i in range(len(self.content)):
                if math.ceil(self.header_style.font_size / 1.6666667) * len(temp_str[:-i - 1]) <= (pdf.pdf._pagesize[0]
                                                                                                   - 2 * cm - 1.5 * cm):
                    temp_vector.append(temp_str[:-i - 1])
                    break
            temp_vector.append(temp_str[len(temp_vector[0]):])
        if pdf.cursor.get_y() >= 1.5 * cm:
            pass
        else:
            pdf.pdf.showPage()
            pdf.cursor.move(x=3 * cm, y=A4[1] - (2.9 * cm))

        if len(temp_vector) <= 0 and len(link) <=0:
            text = Paragraph(temp_content, paragrahp_style)
            text.splitOn(pdf.pdf, (math.ceil(self.header_style.font_size / 1.6666667) * len(self.content)),
                         24)
            text.drawOn(pdf.pdf, pdf.cursor.get_x() + self.header_style.margin_left, pdf.cursor.get_y() - self.header_style.margin_top)
            pdf.cursor.move(x=3 * cm, y=pdf.cursor.get_y() - 0.75 * cm - self.header_style.margin_bottom)
        elif len(temp_vector) > 0 and len(link) <= 0:
            for k in temp_vector:
                text = Paragraph(k, paragrahp_style)
                text.splitOn(pdf.pdf, (math.ceil(self.header_style.font_size / 1.6666667) * len(self.content)),
                             24)
                text.drawOn(pdf.pdf, pdf.cursor.get_x() + self.header_style.margin_left,
                            pdf.cursor.get_y() - self.header_style.margin_top)
                pdf.cursor.move(x=3 * cm, y=pdf.cursor.get_y() - 0.75 * cm - self.header_style.margin_bottom)
        elif len(link) > 0:
            text = Paragraph(self.content, paragrahp_style)
            text.splitOn(pdf.pdf, (math.ceil(self.header_style.font_size / 1.6666667) * len(self.content)),
                         24)
            text.drawOn(pdf.pdf, pdf.cursor.get_x() + self.header_style.margin_left,
                        pdf.cursor.get_y() - self.header_style.margin_top)
            pdf.cursor.move(x=3 * cm, y=pdf.cursor.get_y() - 0.75 * cm - self.header_style.margin_bottom)

    def to_html(self):
        return "<p align=" + str(self.header_style.align) + " style='font-size: " + str(self.header_style.font_size) + \
               "pt ; font-family: " + str(self.header_style.font_family) + " ; background: " + \
               str(self.header_style.bgcolor) + " ; color: " + str(self.header_style.color) + " ; margin-top: " + \
               str(self.header_style.margin_top) + "px; margin-bottom: " + str(self.header_style.margin_bottom) + \
               "px; margin-left: " + str(self.header_style.margin_left) + "px; margin-right: " + \
               str(self.header_style.margin_right) + "px;' id='" + str(self.header_style.id) + "'>" + self.content + \
               "</p>\n"

    def set_style(self, style=RGStyle()):
        self.header_style = style

    def get_style(self):
        return self.header_style

    def get_text(self):
        return self.content
