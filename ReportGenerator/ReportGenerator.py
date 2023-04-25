try:
    from .RGStyle import RGStyle, RGTableStyle
    from .RGTable import RGTable, RGCell
    from .RGHeader import RGHeader
    from .RGText import RGText
    from .RGImage import RGImage
    from .RGChart import RGChart
    from .RGBreakPage import BreakPage, ResizePage
    from .RGPDF import PDF
    from .RGHeadlines import json, copy, timedelta, time, re, math, A4, mm, cm, sort_col, find_max_len_str
except ImportError:
    from RGStyle import RGStyle, RGTableStyle
    from RGTable import RGTable, RGCell
    from RGHeader import RGHeader
    from RGText import RGText
    from RGImage import RGImage
    from RGChart import RGChart
    from RGBreakPage import BreakPage, ResizePage
    from RGPDF import PDF
    from RGHeadlines import json, copy, timedelta, time, re, math, A4, mm, cm, sort_col, find_max_len_str


class ReportGenerator:

    def __init__(self, objects=None):
        if objects:
            self.objects = objects
        else:
            self.objects = list()

    def read_from_json_file(self, name_file: list):

        if len(name_file) > 0:
            for i in range(len(name_file)):
                with open(name_file[i], "r", encoding='utf-8') as read_file:
                    temp = json.load(read_file)
                data_json = temp["body"]

                for elem in data_json:
                    if elem.get('type') == 'Header':
                        if elem.get('table') != 0:
                            self.add_header(elem.get('text'), elem.get('level'), RGStyle(font_size=elem.get('fontSize'),
                                                                                         font_type=elem.get('fontName'),
                                                                                         font_color=elem.get(
                                                                                             'textColor'),
                                                                                         background_color=elem.get(
                                                                                             'backColor'),
                                                                                         align=elem.get('align'),
                                                                                         margin_top=elem.get(
                                                                                             'marginTop') / cm,
                                                                                         margin_bottom=elem.get(
                                                                                             'marginBottom') / cm,
                                                                                         margin_left=elem.get(
                                                                                             'marginLeft') / cm,
                                                                                         margin_right=elem.get(
                                                                                             'marginRight') / cm,
                                                                                         id=elem.get('id')
                                                                                         ), table_h=elem.get('table'))
                    elif elem.get('type') == 'Main_text':
                        self.add_text(elem.get('text'),
                                      RGStyle(font_size=elem.get('fontSize'), font_type=elem.get('fontName'),
                                              font_color=elem.get('textColor'),
                                              background_color=elem.get('backColor'),
                                              align=elem.get('align'),
                                              margin_top=elem.get('marginTop') / cm,
                                              margin_bottom=elem.get('marginBottom') / cm,
                                              margin_left=elem.get('marginLeft') / cm,
                                              margin_right=elem.get('marginRight') / cm,
                                              id=elem.get('id')
                                              ))
                    elif elem.get('type') == 'table':
                        count_row = len(elem.get('Data'))
                        count_column = len((elem.get('Data'))[0].get('row'))

                        header_line = elem.get('header_line')
                        if header_line is not None:
                            temp_table = self.add_table(count_row, count_column, elem.get('id'),
                                                        elem.get('header_line'))
                        else:
                            temp_table = self.add_table(count_row, count_column, elem.get('id'), 0)

                        i_ = 0
                        list_merge = list()
                        for t in elem.get('Data'):
                            j_ = 0
                            for j in t.get('row'):
                                if j.get('merge') == 0:
                                    if j.get('colspan') > 1 or j.get('rowspan') > 1:
                                        list_merge.append([i_, j_, j.get('colspan'), j.get('rowspan')])
                                    if j.get('name') is not None and j.get('type') == 'image':
                                        width = j.get('width')
                                        height = j.get('height')
                                        temp_table.set_cell_complex_value(i_, j_,
                                                                          RGImage(j.get('name'),
                                                                                  100 if width > 100 else width,
                                                                                  200 if height > 200 else height))
                                    else:
                                        temp_table.set_cell_value(i_, j_, j.get('text'))
                                        temp_table.set_cell_style(i_, j_, RGStyle(font_size=j.get('fontSize'),
                                                                                  font_type=j.get('fontName'),
                                                                                  font_color=j.get('textColor'),
                                                                                  background_color=j.get('backColor'),
                                                                                  align=j.get('align'),
                                                                                  margin_top=j.get('marginTop') / cm,
                                                                                  margin_bottom=j.get('marginBottom') / cm,
                                                                                  margin_left=j.get('marginLeft') / cm,
                                                                                  margin_right=j.get('marginRight') / cm,
                                                                                  colspan=j.get('colspan'),
                                                                                  rowspan=j.get('rowspan'),
                                                                                  id=j.get('id')))

                                j_ += 1
                            i_ += 1

                        for k in list_merge:
                            temp_table.merge_cells(k[0], k[1], k[2], k[3])
                    elif elem.get('type') == 'graph':
                        self.add_image(elem.get('nameChart'), elem.get('width'), elem.get('height'))
                    elif elem.get('type') == 'image':
                        width = elem.get('width')
                        height = elem.get('height')
                        self.add_image(elem.get('name'), 150 if width > 150 else width, 200 if height > 200 else height)
                self.add_break_page()

    def add_header(self, text_content: str = " ", level: int = 1, style=RGStyle(), table_h: int = 0) -> RGHeader:
        self.objects.append(RGHeader(text_content, level, style, table=table_h))
        return self.objects[-1]

    def add_text(self, text_content: str = " ", style=RGStyle()):
        self.objects.append(RGText(text_content, style))

    def add_image(self, name_image_file: str = " ", width_image: int = 100, height_image: int = 100):
        self.objects.append(RGImage(name_image_file, 300 if width_image > 300 else width_image,
                                    600 if height_image > 600 else height_image))

    def add_table(self, rows: int = 1, columns: int = 1, name: str = "", header_line: int = 1,
                  style=RGTableStyle()) -> RGTable:
        self.objects.append(RGTable(rows, columns, name, header_line, style))
        return self.objects[-1]

    def add_break_page(self):
        self.objects.append(BreakPage())
        self.objects.append(ResizePage('portrait'))

    def set_page_size(self, orientation='portrait'):
        self.objects.append(ResizePage(orientation))

    def set_table_cell_value(self, id_table, row, column, value):
        self.objects[id_table].set_cell_value(row, column, value)

    def set_table_cell_style(self, id_table, row, column, value):
        self.objects[id_table].set_cell_style(row, column, value)

    def get_element(self, index: int):
        return self.objects[index]

    def add_chart(self, name_chart, type_chart, data_chart, axis_name, width=400, height=200):
        self.objects.append(RGChart(name_chart, type_chart, data_chart, axis_name, width, height))

    def add_row_in_table(self, id_table, text_in_cell, cell_style):
        temp_data = []
        for i in range(self.objects[id_table].columns):
            temp_data.append(RGCell(text_in_cell, cell_style))
        self.objects[id_table].data.append(temp_data)

    @staticmethod
    def check_page(start: int, end: int, list_obj):
        index = 0
        for i in range(start, end):
            if type(list_obj[i]) == RGTable:
                index = 1
                max_width_size_cell = []
                for n in range(list_obj[i].get_column_count()):
                    max_width_size_cell.append(0)
                tmp_str = []
                for k in range(list_obj[i].get_row_count()):
                    j__ = 0
                    for j in range(list_obj[i].get_column_count()):
                        if list_obj[i].data[k][j].complex_value is not None:
                            if max_width_size_cell[j__] < list_obj[i].data[k][j].complex_value.width_image + 2 * mm:
                                max_width_size_cell[j__] = list_obj[i].data[k][j].complex_value.width_image + 2 * mm
                            if max_width_size_cell[j__] < list_obj[i].data[k][j].complex_value.height_image + 2 * mm:
                                max_width_size_cell[j__] = list_obj[i].data[k][j].complex_value.height_image + 2 * mm
                            continue
                        if list_obj[i].data[k][j].merge == 0:
                            if list_obj[i].data[k][j].style.rowspan == 1 and list_obj[i].data[k][
                                j].style.colspan == 1 \
                                    and str(list_obj[i].data[k][j].value) != "":
                                if str(list_obj[i].data[k][j].value).find("\n"):
                                    temp_value = list_obj[i].data[k][j].value
                                    if list_obj[i].data[k][j].value.find("\n") != len(list_obj[i].data[k][j].value) - 1:
                                        if list_obj[i].data[k][j].value[list_obj[i].data[k][j].value.find("\n") + 1] == " ":
                                            temp_value = list_obj[i].data[k][j].value[:list_obj[i].data[k][j].value.find("\n") + 1] \
                                                         + list_obj[i].data[k][j].value[list_obj[i].data[k][j].value.find("\n") + 2:]
                                    tmp_str = temp_value.split("\n")

                                lentmpstr = find_max_len_str(tmp_str)

                                if lentmpstr > 40:
                                    lentmpstr = 40

                                if max_width_size_cell[j__] < (((math.ceil(list_obj[i].data[k][j].style.font_size / 1.66667))
                                * lentmpstr + list_obj[i].data[k][j].style.margin_left +
                                                             list_obj[i].data[k][j].style.margin_right)):
                                    max_width_size_cell[j__] = (math.ceil(list_obj[i].data[k][j].style.font_size / 1.66667)) \
                                    * lentmpstr + list_obj[i].data[k][j].style.margin_left + \
                                                            list_obj[i].data[k][j].style.margin_right - 1
                            elif max_width_size_cell[j__] != 0:
                                pass
                            else:
                                max_width_size_cell[j__] = 0
                            tmp_str.clear()
                        j__ += 1
                summ = 0
                for z in max_width_size_cell:
                    summ += z
                if summ > A4[0]:
                    if start == 0:
                        list_obj.insert(start, ResizePage("landscape"))
                    else:
                        list_obj.insert(start + 1, ResizePage("landscape"))
                elif summ < A4[0]:
                    if start == 0:
                        list_obj.insert(start, ResizePage("portrait"))
                    else:
                        list_obj.insert(start + 1, ResizePage("portrait"))
            elif type(list_obj[i]) == RGImage:
                index = 1
                if list_obj[i].width_image > A4[0]:
                    if start == 0:
                        list_obj.insert(start, ResizePage("landscape"))
                    else:
                        list_obj.insert(start + 1, ResizePage("landscape"))
                elif list_obj[i].width_image < A4[0]:
                    if start == 0:
                        list_obj.insert(start, ResizePage("portrait"))
                    else:
                        list_obj.insert(start + 1, ResizePage("portrait"))
            if index == 0 and i == end - 1:
                if start == 0:
                    list_obj.insert(start, ResizePage("portrait"))
                else:
                    list_obj.insert(start + 1, ResizePage("portrait"))

    def save_to_text(self, name_file: str):
        outstr = ''
        for i in self.objects:
            outstr += i.to_text()
            outstr += "\n"
        file = open(name_file + ".txt", 'w')
        file.write(outstr)
        file.close()

    def save_to_pdf(self, name_file: str):
        if name_file.find('.pdf') == -1:
            name_file += ".pdf"
        pdf_doc = PDF(file_name=name_file)
        break_page_list = list()
        break_page_list.append(0)
        _size_obj = len(self.objects)
        if _size_obj > 0:
            for i in range(_size_obj):
                if type(self.objects[i]) == BreakPage:
                    break_page_list.append(i)

            for i in range(len(break_page_list)):
                if len(break_page_list) == 1:
                    self.check_page(0, len(self.objects), self.objects)
                elif len(break_page_list) > 1:
                    if i == 0:
                        self.check_page(i, break_page_list[i + 1], self.objects)
                    elif i < len(break_page_list) - 1 and i != 0:

                        self.check_page(break_page_list[i] + 1, break_page_list[i + 1] + i, self.objects)
                    else:
                        self.check_page(break_page_list[i], len(self.objects), self.objects)
                break_page_list.clear()
                break_page_list.append(0)
                for p in range(len(self.objects)):
                    if type(self.objects[p]) == BreakPage:
                        break_page_list.append(p)
            for i in self.objects:
                i.to_pdf(pdf=pdf_doc)
            if type(self.objects[-1]) != BreakPage and type(self.objects[-1]) != ResizePage:
                pdf_doc.pdf.showPage()
            pdf_doc.pdf.save()
        else:
            print("PDF is empty")

    def save_to_json(self, name_json_file: str):
        json_list = list()
        json_dict = dict()
        for i in self.objects:
            if type(i) != BreakPage and type(i) != ResizePage:
                json_list.append(i.to_json())
        json_dict.update({'body': json_list, 'name': '%s' % (name_json_file + ".json"), 'type': 'json'})
        if len(json_list) > 0:
            if name_json_file.find('.json') == -1:
                name_json_file = name_json_file + ".json"
            with open(name_json_file, "w") as write_file:
                json.dump(json_dict, write_file, indent=4)
        else:
            print("JSON is empty")

    def save_to_html(self, name_html_file: str):
        html_list = list()
        for i in self.objects:
            if i.__class__ == RGImage or i.__class__ == RGTable:
                html_list.append(i.to_html(name_html_file))
            else:
                html_list.append(i.to_html())
        if len(html_list) > 0:
            file = open(name_html_file + ".html", "w")
            html_str = "<!DOCTYPE html><head><title>{name}</title>".format(name=name_html_file)
            html_str += "<meta charset='utf-8' content='text/html' " \
                        "http_equiv='Content-Type'></meta>\n<style type='text/css'>p, li { white-space: pre-wrap; }\n" \
                        "img.all_foto {text-align: center; margin-top: 2; margin-bottom: 2px; margin-left: 5px; " \
                        "margin-right: 5px;}\n" \
                        "</style>\n" \
                        "<script type='text/javascript'> function openImageWindow(src) {var image = new Image(); " \
                        "image.src = src; var width = image.width; var height = image.height; " \
                        "window.open(src,'Image','width=' + width + ',height=' + height); }</script>\n</head>\n<body>\n"
            file.write(html_str)
            for i in html_list:
                file.write(i)
            file.write("</body>\n</html>")
            file.close()
        else:
            print("HTML is empty")
