try:
    from .RGHeadlines import mm, cm, A4, landscape, math, os, shutil
    from .RGPDF import PDF
except ImportError:
    from RGHeadlines import mm, cm, A4, landscape, math, os, shutil
    from RGPDF import PDF


class RGImage:

    def __init__(self, name=str('NONE'), width=int(100), height=int(100)):
        self.name_image = name
        self.width_image = width
        self.height_image = height

    def to_text(self):
        return self.name_image

    def to_json(self):
        return {'type': 'image', 'name': self.name_image, 'width': self.width_image, 'height': self.height_image,
                'alt': "NAN", 'id': self.name_image, 'align': "center"}

    def to_pdf(self, pdf):

        y = 0
        if (pdf.cursor.get_y() - self.height_image) < 2 * cm and pdf.get_page_size()[1] == 'landscape':
            pdf.pdf.showPage()
            pdf.set_position_cursor(X=3 * cm, Y=landscape(A4)[1] - (2 * cm))
        elif (pdf.cursor.get_y() - self.height_image) < 2 * cm and pdf.get_page_size()[1] == 'portrait':
            pdf.pdf.showPage()
            pdf.set_position_cursor(X=3 * cm, Y=A4[1] - (2 * cm))

        if self.width_image > pdf.pdf._pagesize[0] - (math.ceil(pdf.pdf._pagesize[0] / 2 - self.width_image / 2)) \
                and pdf.get_page_size()[1] == 'portrait':
            pdf.pdf.showPage()
            pdf.set_page_size("A4", "landscape")
            pdf.set_position_cursor(X=3 * cm, Y=landscape(A4)[1] - (2 * cm))
        elif self.width_image < pdf.pdf._pagesize[0] - (math.ceil(pdf.pdf._pagesize[0] / 2 - self.width_image / 2)) \
                and pdf.get_page_size()[1] == 'landscape':
            pdf.set_position_cursor(X=3 * cm, Y=landscape(A4)[1] - (2 * cm))
        else:
            pdf.set_page_size("A4", "portrait")

        y = pdf.cursor.get_y() - self.height_image
        pdf.pdf.drawImage(self.name_image, math.ceil(pdf.pdf._pagesize[0] / 2 - self.width_image / 2),
                          y, self.width_image, self.height_image)

        pdf.set_position_cursor(3 * cm, pdf.cursor.get_y() - self.height_image - 12)

    def to_html(self, name_html_file):
        tmp_index = name_html_file.rfind("\\")
        tmp_index_1 = name_html_file.rfind('/')
        if tmp_index != -1:
            path = name_html_file[:tmp_index]
            local_path_image = os.getcwd()
            if os.path.exists(path + "\\Source") is False:
                os.mkdir(path + "\\Source")
            else:
                pass
            if self.name_image.rfind('/') != -1:
                shutil.copyfile(self.name_image, path + '/Source/' + self.name_image[self.name_image.rfind('/') + 1:])
                path_image = path + '/Source/' + self.name_image[self.name_image.rfind('/') + 1:]
            elif self.name_image.rfind('\\') != -1:
                shutil.copyfile(self.name_image, path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:])
                path_image = path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:]
            else:
                shutil.copyfile(local_path_image + "\\" + self.name_image, path + '\\Source\\' + self.name_image)
                path_image = path + '/Source/' + self.name_image
        elif tmp_index_1 != -1:
            path = name_html_file[:tmp_index_1]
            local_path_image = os.getcwd()
            if os.path.exists(path + "/Source") is False:
                os.mkdir(path + "/Source")
            else:
                pass
            if self.name_image.rfind('/') != -1:
                shutil.copyfile(self.name_image, path + '/Source/' + self.name_image[self.name_image.rfind('/') + 1:])
                path_image = path + '/Source/' + self.name_image[self.name_image.rfind('/') + 1:]
            elif self.name_image.rfind('\\') != -1:
                shutil.copyfile(self.name_image, path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:])
                path_image = path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:]
            else:
                shutil.copyfile(local_path_image + "\\" + self.name_image, path + '/Source/' + self.name_image)
                path_image = path + '/Source/' + self.name_image
        else:
            path = os.getcwd()
            if os.path.exists(path + "\\Source") is False:
                os.mkdir(path + "\\Source")
            else:
                pass
            if self.name_image.rfind('/') != -1:
                shutil.copyfile(self.name_image, path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:])
                path_image = path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:]
            elif self.name_image.rfind('\\') != -1:
                shutil.copyfile(self.name_image, path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:])
                path_image = path + '\\Source\\' + self.name_image[self.name_image.rfind('\\') + 1:]
            else:
                shutil.copyfile(path + "\\" + self.name_image, path + '\\Source\\' + self.name_image)
                path_image = path + '\\Source\\' + self.name_image

        return "<img class='all_foto' src='" + './Source/' + os.path.basename(path_image) + "' width='" + \
               str(self.width_image) + "' height='" + str(self.height_image) + "'alt='NAN' id='" + \
               self.name_image + "' onclick = 'openImageWindow(this.src);' />"
