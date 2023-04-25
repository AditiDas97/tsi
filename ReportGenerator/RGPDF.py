try:
    from .RGHeadlines import mm, cm, A4, landscape, canvas, dict_format_page
except ImportError:
    from RGHeadlines import mm, cm, A4, landscape, canvas, dict_format_page


class Cursor:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, x, y):
        if self.x != x or self.y != y:
            self.x = x
            self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class PDF:

    def __init__(self, file_name=str(""), x=3 * cm, y=A4[1] - (2.9 * cm), name_format='A4',
                 orientation='portrait'):
        self.pdf = canvas.Canvas(file_name)
        self.cursor = Cursor(x, y)
        self.pdf.setPageSize(dict_format_page.get(orientation).get(name_format))
        self.page_size = [name_format, orientation]

    def set_position_cursor(self, X, Y):
        self.cursor.move(X, Y)

    def set_page_size(self, name_format='A4', orientation='landscape'):
        self.pdf.setPageSize(dict_format_page.get(orientation).get(name_format))
        self.page_size = [name_format, orientation]

    def get_page_size(self):
        return self.page_size
