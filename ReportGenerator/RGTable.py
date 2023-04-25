try:
    from .RGHeadlines import mm, cm, Rect, canvas, landscape, A4, math, copy, find_max_len_str
    from .RGStyle import RGTableStyle, RGStyle
    from .RGPDF import PDF
    from .RGImage import RGImage
except ImportError:
    from RGHeadlines import mm, cm, Rect, canvas, landscape, A4, math, copy, find_max_len_str
    from RGStyle import RGTableStyle, RGStyle
    from RGPDF import PDF
    from RGImage import RGImage


def search_divider(len_str):
    divider = 1
    if len_str == 2:
        divider = 2.2
    elif len_str == 3:
        divider = 2
    elif 4 <= len_str < 20:
        divider = 1.15
    elif len_str >= 20:
        divider = 1.045
    return divider


class RGCell:
    def __init__(self, val=str(), style=RGStyle()):
        self.value = str(val)
        self.style = style
        self.merge = 0
        self.complex_value = None

    def get_value(self):
        return self.value


class RGTable:

    @staticmethod
    def fill_table(self_rows, self_columns):
        data = list()
        for i in range(self_rows):
            tmp = [RGCell(str(""), RGStyle()) for j in range(self_columns)]
            data.append(tmp)
        return data

    @staticmethod
    def draw_cell(self_data, i, j, positionCell, pdf, maxWidthSizeCell, maxHeightSizeCell, maxMergeWidthSizeCell):
        shiftWidth = 0
        shiftHeight = 0
        temp_font_name = ""
        tmpStr = []
        tmpStr_2 = []

        if self_data[i][j].value.find("\n"):
            if self_data[i][j].value.find("\n") != len(self_data[i][j].value) - 1:
                if self_data[i][j].value[self_data[i][j].value.find("\n") + 1] == " ":
                    self_data[i][j].value = self_data[i][j].value[:self_data[i][j].value.find("\n") + 1] \
                                      + self_data[i][j].value[self_data[i][j].value.find("\n") + 2:]
            tmpStr = self_data[i][j].value.split("\n")
            max_size = int((int(maxWidthSizeCell[j]) - self_data[i][j].style.margin_left -
                            self_data[i][j].style.margin_right)/((math.ceil(self_data[i][j].style.font_size / 1.66667)))
                           * self_data[i][j].style.colspan) + 4

            for st in tmpStr:
                if len(st) > max_size:
                    tmpStr_2.append(st[:max_size - 1])
                    if len(st[max_size - 1:]) > max_size:
                        tmpStr_2.append(st[max_size - 1:len(st[max_size - 1:])])
                        tmpStr_2.append(st[len(st[max_size - 1:]):])
                    else:
                        tmpStr_2.append(st[max_size - 1:])
                else:
                    tmpStr_2.append(st)

        pdf.pdf.setFillColor(self_data[i][j].style.bgcolor)
        pdf.pdf.setStrokeColor("black")

        if self_data[i][j].style.colspan == 1 and self_data[i][j].style.rowspan == 1:
            pdf.pdf.rect(positionCell, pdf.cursor.get_y(),
                         maxWidthSizeCell[j], maxHeightSizeCell[i], fill=1)
        elif self_data[i][j].style.colspan > 1 and self_data[i][j].style.rowspan == 1:
            for k in range(j, j + self_data[i][j].style.colspan):
                shiftWidth += maxWidthSizeCell[k]
            pdf.pdf.rect(positionCell, pdf.cursor.get_y(),
                         shiftWidth, maxHeightSizeCell[i], fill=1)
        elif self_data[i][j].style.colspan == 1 and self_data[i][j].style.rowspan > 1:
            for k in range(i, i + self_data[i][j].style.rowspan):
                shiftHeight += maxHeightSizeCell[k]
            pdf.pdf.rect(positionCell, pdf.cursor.get_y() -
                         shiftHeight + maxHeightSizeCell[i + self_data[i][j].style.rowspan - 1],
                         maxWidthSizeCell[j], shiftHeight, fill=1)
        else:
            for k in range(i, i + self_data[i][j].style.rowspan):
                shiftHeight += maxHeightSizeCell[k]
            for k in range(j, j + self_data[i][j].style.colspan):
                shiftWidth += maxWidthSizeCell[k]
            pdf.pdf.rect(positionCell, pdf.cursor.get_y() -
                         shiftHeight + maxHeightSizeCell[i + self_data[i][j].style.rowspan - 1],
                         shiftWidth, shiftHeight, fill=1)

        if self_data[i][j].style.font_family == 'Courier new':
            temp_font_name = 'Courier'
        elif self_data[i][j].style.font_family == 'Arial':
            temp_font_name = 'Helvetica'
        elif self_data[i][j].style.font_family == 'Times' or \
                self_data[i][j].style.font_family == 'Times New Roman':
            temp_font_name = 'Times-Roman'
        textobject = pdf.pdf.beginText()

        if (self_data[i][j].style.align == 'center'):
            if len(tmpStr_2) <= 1 and self_data[i][j].style.colspan == 1:
                textobject.setTextOrigin((positionCell + maxWidthSizeCell[j] / 2) + 1 -
                                         (((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(
                                             self_data[i][j].value)) / 2.2),
                                         pdf.cursor.get_y() + maxHeightSizeCell[i] / 2.2)
                textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                textobject.setFillColor(self_data[i][j].style.color)
                textobject.textLine(self_data[i][j].value)
            elif len(tmpStr_2) <= 1 and self_data[i][j].style.colspan > 1:
                width_merge_cell = 0
                for count in maxMergeWidthSizeCell:
                    if count[0] == i and count[1] == j:
                        width_merge_cell = count[3]
                textobject.setTextOrigin((positionCell + width_merge_cell / 2) + 1 -
                                         (((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(
                                             self_data[i][j].value)) / 2.2),
                                         pdf.cursor.get_y() + maxHeightSizeCell[i] / 3)
                textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                textobject.setFillColor(self_data[i][j].style.color)
                textobject.textLine(self_data[i][j].value)
            elif len(tmpStr_2) > 1 and self_data[i][j].style.colspan == 1:
                for line_str in range(len(tmpStr_2)):
                    textobject.setTextOrigin((positionCell + maxWidthSizeCell[j] / 2) + 1 -
                                             (((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(
                                                 tmpStr_2[line_str])) / 2.2),
                                             pdf.cursor.get_y() + self_data[i][j].style.margin_bottom + maxHeightSizeCell[
                                                 i] / search_divider(len(tmpStr_2)) - (
                                                 math.ceil(self_data[i][j].style.font_size / 1.66667)) * 2 * line_str)
                    textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                    textobject.setFillColor(self_data[i][j].style.color)
                    textobject.textLine(tmpStr_2[line_str])
            else:
                width_merge_cell = 0
                for count in maxMergeWidthSizeCell:
                    if count[0] == i and count[1] == j:
                        width_merge_cell = count[3]
                for line_str in range(len(tmpStr_2)):
                    textobject.setTextOrigin((positionCell + width_merge_cell / 2) + 1 -
                                             (((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(
                                                 self_data[i][j].value)) / 2.2),
                                             pdf.cursor.get_y() + self_data[i][j].style.margin_bottom + maxHeightSizeCell[
                                                 i] / search_divider(len(tmpStr_2)) - (
                                                 math.ceil(self_data[i][j].style.font_size / 1.66667)) * 2 * line_str)
                    textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                    textobject.setFillColor(self_data[i][j].style.color)
                    textobject.textLine(tmpStr_2[line_str])

        elif self_data[i][j].style.align == 'left':
            if len(tmpStr_2) <= 1:
                textobject.setTextOrigin(positionCell + self_data[i][j].style.margin_left,
                                         pdf.cursor.get_y() + maxHeightSizeCell[i] / 2.2)
                textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                textobject.setFillColor(self_data[i][j].style.color)
                textobject.textLine(self_data[i][j].value)
            else:
                for line_str in range(len(tmpStr_2)):
                    textobject.setTextOrigin(positionCell + self_data[i][j].style.margin_left,
                                             pdf.cursor.get_y() - self_data[i][j].style.margin_top
                                             + self_data[i][j].style.margin_bottom +
                                             maxHeightSizeCell[i] / search_divider(len(tmpStr_2)) - (
                                                 math.ceil(self_data[i][j].style.font_size / 1.66667)) * 2 * line_str)
                    textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                    textobject.setFillColor(self_data[i][j].style.color)
                    textobject.textLine(tmpStr_2[line_str])

        elif self_data[i][j].style.align == "right":
            if len(tmpStr_2) <= 1 and self_data[i][j].style.colspan == 1:
                textobject.setTextOrigin(positionCell + maxWidthSizeCell[j] + self_data[i][j].style.margin_left -
                                         self_data[i][j].style.margin_right -
                                         ((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(self_data[i][j].value)),
                                         pdf.cursor.get_y() + maxHeightSizeCell[i] / 2.2)
                textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                textobject.setFillColor(self_data[i][j].style.color)
                textobject.textLine(self_data[i][j].value)
            elif len(tmpStr_2) <= 1 and self_data[i][j].style.colspan > 1:
                width_merge_cell = 0
                for count in maxMergeWidthSizeCell:
                    if count[0] == i and count[1] == j:
                        width_merge_cell = count[3]
                textobject.setTextOrigin(positionCell + width_merge_cell + self_data[i][j].style.margin_left -
                                         self_data[i][j].style.margin_right -
                                        ((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(self_data[i][j].value)),
                                        pdf.cursor.get_y() + maxHeightSizeCell[i] / 2.2)
                textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                textobject.setFillColor(self_data[i][j].style.color)
                textobject.textLine(self_data[i][j].value)
            elif len(tmpStr_2) > 1 and self_data[i][j].style.colspan == 1:
                for line_str in range(len(tmpStr_2)):
                    textobject.setTextOrigin(positionCell + maxWidthSizeCell[j] + self_data[i][j].style.margin_left -
                                             self_data[i][j].style.margin_right -
                                         ((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(line_str)),
                                             pdf.cursor.get_y() - self_data[i][j].style.margin_top
                                             + self_data[i][j].style.margin_bottom +
                                             maxHeightSizeCell[i] / search_divider(len(tmpStr_2)) - (
                                                 math.ceil(self_data[i][j].style.font_size / 1.66667)) * 2 * line_str)
                    textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                    textobject.setFillColor(self_data[i][j].style.color)
                    textobject.textLine(tmpStr_2[line_str])
            else:
                for line_str in range(len(tmpStr_2)):
                    width_merge_cell = 0
                    for count in maxMergeWidthSizeCell:
                        if count[0] == i and count[1] == j:
                            width_merge_cell = count[3]
                    textobject.setTextOrigin(positionCell + width_merge_cell + self_data[i][j].style.margin_left -
                                             self_data[i][j].style.margin_right -
                                             ((math.ceil(self_data[i][j].style.font_size / 1.66667)) * len(line_str)),
                                             pdf.cursor.get_y() - self_data[i][j].style.margin_top
                                             + self_data[i][j].style.margin_bottom +
                                             maxHeightSizeCell[i] / search_divider(len(tmpStr_2)) - (
                                                 math.ceil(self_data[i][j].style.font_size / 1.66667)) * 2 * line_str)
                    textobject.setFont(temp_font_name, self_data[i][j].style.font_size)
                    textobject.setFillColor(self_data[i][j].style.color)
                    textobject.textLine(tmpStr_2[line_str])

        pdf.pdf.drawText(textobject)

    def __init__(self, rows: int, columns: int, name: str = "", header_line: int = 1, tbl_style=RGTableStyle()):
        self.rows = rows
        self.columns = columns
        self.name = name
        self.table_style = tbl_style
        self.header_line = header_line
        self.data = self.fill_table(self.rows, self.columns)

    def merge_cells(self, row, column, numRows, numCols):
        if numRows <= 0:
            numRows = 1
        if numCols <= 0:
            numCols = 1
        if 0 <= row < self.rows and 0 <= column < self.columns:
            if (0 < (row + numCols) <= self.rows) and (0 < (column + numRows) <= self.columns):
                self.data[row][column].style.rowspan = numCols
                self.data[row][column].style.colspan = numRows
                i = row
                j = column
                if i > 0:
                    numCols += i
                if j > 0:
                    numRows += j
                for i in range(i, numCols):
                    j = column
                    for j in range(j, numRows):
                        if i == row and j == column:
                            continue
                        else:
                            self.data[i][j].merge = 1
            else:
                print("going beyond the table")

    def to_text(self):
        t_str = ''
        for i in range(self.rows):
            for j in range(self.columns):
                t_str += "|" + str(self.data[i][j].value) + '|'
            t_str += '\n'
        return t_str

    def to_json(self):
        temp_data = list()
        if self.rows > 0:
            for row in range(self.rows):
                tempOneRow = list()
                for i in range(self.columns):
                    if self.data[row][i].merge == 0:
                        tempOneRow.append({'text': self.data[row][i].value,
                                           'id': self.data[row][i].style.id,
                                           'fontSize': self.data[row][i].style.font_size,
                                           'fontName': self.data[row][i].style.font_family,
                                           'textColor': self.data[row][i].style.color,
                                           'marginRight': self.data[row][i].style.margin_right,
                                           'marginLeft': self.data[row][i].style.margin_left,
                                           'marginBottom': self.data[row][i].style.margin_bottom,
                                           'marginTop': self.data[row][i].style.margin_top,
                                           'backColor': self.data[row][i].style.bgcolor,
                                           'rowspan': self.data[row][i].style.rowspan,
                                           'colspan': self.data[row][i].style.colspan,
                                           'align': self.data[row][i].style.align, 'merge': self.data[row][i].merge
                                           })
                    elif self.data[row][i].merge == 1:
                        tempOneRow.append({'text': '', 'merge': self.data[row][i].merge})
                temp_data.append({'row': tempOneRow, 'type': 'row'})
            return {'Data': temp_data, 'type': 'table',
                    'id': self.name + "table", 'border': self.table_style.border, 'cellspacing': 0,
                    'border_collapse': 'collapse', 'align': self.table_style.table_align,
                    'header_line': self.header_line}
        else:
            return {'Data': temp_data, 'type': 'table', 'id': self.name + "table",
                    'border': self.table_style.border, 'cellspacing': 0,
                    'border_collapse': 'collapse', 'align': self.table_style.table_align,
                    'header_line': self.header_line}

    def to_pdf(self, pdf):

        maxHeightSizeCell = []
        maxWidthSizeCell = []
        maxMergeWidthSizeCell = []
        tmpStr = []
        tmpStr_2 = []
        lentmpStr = []
        summ = 0
        summHeight = 0
        positionCell = 0

        for j in range(self.columns):
            maxWidthSizeCell.append(0)

        for i in range(self.rows):
            maxHeightSizeCell.append(0)

        for i in range(self.rows):
            for j in range(self.columns):

                if self.data[i][j].complex_value is not None:
                    if maxWidthSizeCell[j] < self.data[i][j].complex_value.width_image + 2 * mm:
                        maxWidthSizeCell[j] = self.data[i][j].complex_value.width_image + 2 * mm
                    if maxHeightSizeCell[i] < self.data[i][j].complex_value.height_image + 2 * mm:
                        maxHeightSizeCell[i] = self.data[i][j].complex_value.height_image + 2 * mm
                    continue

                if self.data[i][j].value.find("\n"):
                    temp_value = self.data[i][j].value
                    if self.data[i][j].value.find("\n") != len(self.data[i][j].value) - 1:
                        if self.data[i][j].value[self.data[i][j].value.find("\n") + 1] == " ":
                            temp_value = self.data[i][j].value[:self.data[i][j].value.find("\n") + 1] \
                                                    + self.data[i][j].value[self.data[i][j].value.find("\n") + 2:]
                    tmpStr = temp_value.split("\n")

                lentmpStr = find_max_len_str(tmpStr)

                if lentmpStr > 40:
                    lentmpStr = 40

                if self.data[i][j].style.rowspan == 1 and self.data[i][j].style.colspan == 1:
                    if (maxWidthSizeCell[j] < (math.ceil(self.data[i][j].style.font_size / 1.66667)) * lentmpStr
                            + self.data[i][j].style.margin_left + self.data[i][j].style.margin_right):
                        maxWidthSizeCell[j] = ((math.ceil(self.data[i][j].style.font_size / 1.66667))
                                               * lentmpStr + self.data[i][j].style.margin_left + self.data[i][
                                                   j].style.margin_right) - 0.05 * cm

                    max_size = int((int(maxWidthSizeCell[j]) - self.data[i][j].style.margin_left -
                                    self.data[i][j].style.margin_right) / (
                                       (math.ceil(self.data[i][j].style.font_size / 1.66667))) *
                                   self.data[i][j].style.colspan) + 3

                    for st in tmpStr:
                        if len(st) > max_size:
                            tmpStr_2.append(st[:max_size - 1])
                            if len(st[max_size - 1:]) > max_size:
                                tmpStr_2.append(st[max_size - 1:len(st[max_size - 1:])])
                                tmpStr_2.append(st[len(st[max_size - 1:]):])
                            else:
                                tmpStr_2.append(st[max_size - 1:])
                        else:
                            tmpStr_2.append(st)

                    if (maxHeightSizeCell[i] < (math.ceil(self.data[i][j].style.font_size / 1.66667)
                                                + self.data[i][j].style.margin_bottom + self.data[i][
                                                    j].style.margin_top) * len(tmpStr_2)):
                        maxHeightSizeCell[i] = (math.ceil(self.data[i][j].style.font_size / 1.66667)
                                                + self.data[i][j].style.margin_bottom + self.data[i][
                                                    j].style.margin_top) * len(tmpStr_2)
                else:
                    # maxWidthSizeCell[j] = 0
                    maxMergeWidthSizeCell.append([i, j, self.data[i][j].style.colspan])

                tmpStr.clear()
                tmpStr_2.clear()

        i = 0
        temp_cursor_y = pdf.cursor.get_y()
        while i < self.rows:
            for j in range(self.columns):
                if self.data[i][j].complex_value is not None:
                    continue
                if maxHeightSizeCell[i] > temp_cursor_y - 1.5 * cm:
                    new_raw = [RGCell(self.data[i][p].value, RGStyle()) for p in range(self.columns)]
                    new_raw[j].value = ""
                    new_raw_list = self.data[i][j].value.split("\n")
                    size = int((temp_cursor_y) / (math.ceil(self.data[i][j].style.font_size / 1.66667)
                                    + self.data[i][j].style.margin_bottom + self.data[i][j].style.margin_top))

                    if len(new_raw_list) - 1 > size:
                        for index in range(size):
                            new_raw[j].value += new_raw_list[index] + "\n"

                        self.data[i][j].value = ""
                        for index in range(size, len(new_raw_list)):
                            self.data[i][j].value += new_raw_list[index] + "\n"

                        self.insert_row(i)

                        for k in range(self.columns):
                            self.set_cell_value(i, k, new_raw[k].value)
                        maxHeightSizeCell[i] = (math.ceil(self.data[i][j].style.font_size / 1.66667)
                                                + self.data[i][j].style.margin_bottom + self.data[i][
                                                    j].style.margin_top) * (len(new_raw[j].value.split("\n")))

                        count_split = len(self.data[i + 1][j].value.split("\n"))

                        if count_split < 5:
                            count_split = count_split + 5
                        maxHeightSizeCell.insert(i + 1, (math.ceil(self.data[i + 1][j].style.font_size / 1.66667)
                                                         + self.data[i + 1][j].style.margin_bottom + self.data[i + 1][
                                                             j].style.margin_top) * (
                                                             count_split - 1))
                        self.rows += 1
                        i += 1
                    else:
                        del new_raw, new_raw_list, size

            i += 1
        del i, temp_cursor_y

        for i in maxWidthSizeCell:
            summ += i

        for i in maxHeightSizeCell:
            summHeight += i

        mergeSumm = 0
        for cell in maxMergeWidthSizeCell:
            mergeSumm = 0
            for i in range(cell[1], cell[1] + cell[2]):
                mergeSumm += maxWidthSizeCell[i]
            cell.append(mergeSumm)

        if pdf.cursor.get_y() - summHeight < 1.5 * cm and summHeight < A4[1] and pdf.get_page_size()[1] == 'portrait':
            pdf.pdf.showPage()
            pdf.set_position_cursor(X=3 * cm, Y=A4[1] - (2.9 * cm))
        elif pdf.cursor.get_y() - summHeight < 1.5 * cm and summHeight < A4[1] and pdf.get_page_size()[
            1] == 'landscape':
            pdf.pdf.showPage()
            pdf.set_position_cursor(X=3 * cm, Y=landscape(A4)[1] - (2 * cm))

        pdf.set_position_cursor(pdf.cursor.get_x(), pdf.cursor.get_y() - maxHeightSizeCell[0])
        for i in range(self.rows):
            positionCell = math.ceil(pdf.pdf._pagesize[0] / 2 - summ / 2)
            if pdf.cursor.get_y() < cm * 1.5:
                pdf.pdf.showPage()
                if pdf.get_page_size()[1] == "portrait":
                    pdf.set_position_cursor(X=3 * cm, Y=A4[1] - (2.9 * cm))
                elif pdf.get_page_size()[1] == "landscape":
                    pdf.set_position_cursor(X=3 * cm, Y=landscape(A4)[1] - (2 * cm))
                for k in range(self.header_line):
                    for j in range(self.columns):
                        if self.data[k][j].merge == 0:
                            self.draw_cell(self.data, k, j, positionCell, pdf, maxWidthSizeCell,
                                           maxHeightSizeCell, maxMergeWidthSizeCell)
                        positionCell += maxWidthSizeCell[j]
                    pdf.set_position_cursor(pdf.cursor.get_x(), pdf.cursor.get_y() - maxHeightSizeCell[k])
                    positionCell = math.ceil(pdf.pdf._pagesize[0] / 2 - summ / 2)
            for j in range(self.columns):
                if self.data[i][j].complex_value is not None:
                    self.draw_cell(self.data, i, j, positionCell, pdf, maxWidthSizeCell, maxHeightSizeCell,
                                   maxMergeWidthSizeCell)
                    image = self.data[i][j].complex_value
                    pdf.pdf.drawImage(image.name_image, positionCell + 1 * mm, pdf.cursor.get_y() + 1 * mm,
                                      image.width_image, image.height_image)
                elif self.data[i][j].merge == 0:
                    self.draw_cell(self.data, i, j, positionCell, pdf, maxWidthSizeCell, maxHeightSizeCell,
                                   maxMergeWidthSizeCell)
                positionCell += maxWidthSizeCell[j]

            if i < self.rows - 1:
                if pdf.cursor.get_y() < maxHeightSizeCell[i + 1] + 1.5 * cm:
                    if pdf.get_page_size()[1] == "portrait":
                        pdf.pdf.showPage()
                        pdf.set_position_cursor(X=3 * cm, Y=A4[1] - (2.9 * cm))
                    elif pdf.get_page_size()[1] == "landscape":
                        pdf.pdf.showPage()
                        pdf.set_position_cursor(X=3 * cm, Y=landscape(A4)[1] - (2 * cm))
                    if self.header_line > 0:
                        positionCell = math.ceil(pdf.pdf._pagesize[0] / 2 - summ / 2)
                        for k in range(self.header_line):
                            for j in range(self.columns):
                                if self.data[k][j].merge == 0:
                                    self.draw_cell(self.data, k, j, positionCell, pdf, maxWidthSizeCell,
                                                   maxHeightSizeCell, maxMergeWidthSizeCell)
                                positionCell += maxWidthSizeCell[j]
                            pdf.set_position_cursor(pdf.cursor.get_x(), pdf.cursor.get_y())
                if maxHeightSizeCell[i + 1] > maxHeightSizeCell[i] or maxHeightSizeCell[i + 1] < maxHeightSizeCell[i]:
                    pdf.set_position_cursor(pdf.cursor.get_x(), pdf.cursor.get_y() - maxHeightSizeCell[i + 1])
                else:
                    pdf.set_position_cursor(pdf.cursor.get_x(), pdf.cursor.get_y() - maxHeightSizeCell[i])
            else:
                pdf.set_position_cursor(pdf.cursor.get_x(), pdf.cursor.get_y() - maxHeightSizeCell[i])
        pdf.set_position_cursor(X=3 * cm, Y=pdf.cursor.get_y())

    def to_html(self, name_file: str):
        tmpText = "<table id=\"" + self.name + "\" border='3' " \
                    "cellspacing='0' border_collapse='collapse' align='center'>\n<tbody>"

        for i in range(self.rows):
            tmpTr = "<tr>\n"

            for j in range(self.columns):
                if self.data[i][j].merge == 0:
                    tmpTdP = ""
                    strTempVector = list()

                    if self.data[i][j].complex_value is None:
                        if str(self.data[i][j].value).find("\n") != -1:
                            strTempVector = str(self.data[i][j].value).split('\n')
                            tmpTdP = "<td " + "colspan='" + str(self.data[i][j].style.colspan) + "' rowspan='"
                            tmpTdP += str(self.data[i][j].style.rowspan) + "' bgcolor='"
                            tmpTdP += str(self.data[i][j].style.bgcolor) + "' border='10px'>"

                            for k in range(len(strTempVector)):
                                tmpTdP += "\n<p align='" + str(self.data[i][j].style.align) + "' style=\" margin-top: "
                                tmpTdP += str(self.data[i][j].style.margin_top) + "px; margin-bottom: "
                                tmpTdP += str(self.data[i][j].style.margin_bottom) + "px; margin-left: "
                                tmpTdP += str(self.data[i][j].style.margin_left) + "px; margin-right: "
                                tmpTdP += str(self.data[i][j].style.margin_right) + "px; text-indent:0px; \">"
                                tmpTdP += "<span style=\"font-size:" + str(self.data[i][j].style.font_size)
                                tmpTdP += "pt; font-family:'" + str(self.data[i][j].style.font_family) + "' ; background: "
                                tmpTdP += str(self.data[i][j].style.bgcolor) + " ; color: "
                                tmpTdP += str(self.data[i][j].style.color) + "\">" + strTempVector[k] + "</span></p>\n"
                            tmpTr += "</td>" + tmpTdP + "\n"
                        else:
                            tmpTdP += "<td colspan='" + str(self.data[i][j].style.colspan) + "' rowspan='"
                            tmpTdP += str(self.data[i][j].style.rowspan) + "' bgcolor='" + str(
                                self.data[i][j].style.bgcolor)
                            tmpTdP += "' border='10px'>" + "\n<p align=" + str(
                                self.data[i][j].style.align) + " style='font-size: "
                            tmpTdP += str(self.data[i][j].style.font_size) + "pt ; font-family: " + self.data[i][
                                j].style.font_family
                            tmpTdP += " ; background: " + self.data[i][j].style.bgcolor + " ; color: " + self.data[i][
                                j].style.color
                            tmpTdP += " ; margin-top: " + str(self.data[i][j].style.margin_top) + "px; margin-bottom: "
                            tmpTdP += str(self.data[i][j].style.margin_bottom) + "px; margin-left: " + str(
                                self.data[i][j].style.margin_left)
                            tmpTdP += "px; margin-right: " + str(self.data[i][j].style.margin_right) + "px;' id='"
                            tmpTdP += str(self.data[i][j].style.id) + "'>" + str(self.data[i][j].value) + "</p>\n</td>"
                            tmpTr += tmpTdP + "\n"
                    else:
                        tmpTdP += "<td colspan='" + str(self.data[i][j].style.colspan) + "' rowspan='"
                        tmpTdP += str(self.data[i][j].style.rowspan) + "' bgcolor='" + str(
                            self.data[i][j].style.bgcolor)
                        tmpTdP += "' border='10px'>\n" + self.data[i][j].complex_value.to_html(name_file) + "\n</td>"
                        tmpTr += tmpTdP + "\n"
            tmpTr += "</tr>\n"
            tmpText += tmpTr
        tmpText += "</tbody>\n</table> <br>"

        return tmpText

    def get_row_count(self):
        return self.rows

    def get_column_count(self):
        return self.columns

    def set_cell_value(self, row, column, value):
        self.data[row][column].value = str(value)

    def set_cell_complex_value(self, row: int, column: int, image: RGImage):
        self.data[row][column].complex_value = image

    def set_cell_style(self, row, column, style):
        self.data[row][column].style = style

    def set_row_value(self, row, value):
        for i in range(self.columns):
            self.data[row][i].value = str(value)

    def set_column_value(self, column, value):
        for i in range(self.rows):
            self.data[i][column].value = str(value)

    def set_row_style(self, row, style):
        for i in range(self.columns):
            self.data[row][i].style = copy.copy(style)

    def set_column_style(self, column, style):
        for i in range(self.rows):
            self.data[i][column].style = copy.copy(style)

    def set_header_line(self, header):
        if header > 0:
            self.header_line = header
        else:
            self.header_line = 1

    def get_cell_value(self, row, column):
        return self.data[row][column].value

    def get_cell_style(self, row, column):
        return self.data[row][column].style

    def insert_row(self, pos=-1, style=RGStyle()):
        row = []

        for i in range(self.columns):
            row.append(RGCell(str(""), style=RGStyle()))
        if 0 <= pos < self.rows:
            self.data.insert(pos, row)
        else:
            self.data.append(row)
        self.rows += 1

    def insert_column(self, pos=-1, style=RGStyle()):
        column = []

        for i in range(self.rows):
            column.append(RGCell(str(""), style=RGStyle()))
        if 0 <= pos < self.columns:
            for i in range(self.rows):
                self.data[i].insert(pos, column[i])
        else:
            for i in range(self.rows):
                self.data[i].insert(len(self.data[i]) - 1, column[i])
        self.columns += 1
