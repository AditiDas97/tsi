try:
    from .RGHeadlines import mm, cm, inch
except ImportError:
    from RGHeadlines import mm, cm, inch


class RGTableStyle:

    def __init__(self, width=0, height=0, align='center', font_size=9,
                 font_type="Courier new", text_align='center', border=int(3),
                 table_layout='auto', white_space='pre-wrap', border_collapse='collapse'):
        self.width = 0
        self.height = 0
        self.table_align = align
        self.font_size = font_size
        self.font_family = font_type
        self.text_align = text_align
        self.border = border
        self.table_layout = table_layout
        self.white_space = white_space
        self.border_collapse = border_collapse
        self.body_style = 'table-layout: %s ; width: 0 ; white-space: %s ; ' % (self.table_layout, self.white_space)


class RGStyle:

    def __init__(self, font_size: int = 9, font_type: str = "Courier new", font_color='black',
                 background_color='white', align='left', border: str = '2px solid red', margin_top: float = 0.1,
                 margin_bottom: float = 0.2, margin_left: float = 0.1, margin_right: float = 0.001, colspan: int = 1,
                 rowspan: int = 1, id='None'):
        self.font_size = font_size
        self.font_family = font_type
        self.color = font_color
        self.bgcolor = background_color
        self.align = align
        self.border = border
        self.width = 0
        self.height = 0
        self.colspan = colspan
        self.rowspan = rowspan
        self.margin_top = margin_top * cm
        self.margin_bottom = margin_bottom * cm
        self.margin_left = margin_left * cm
        self.margin_right = margin_right * cm
        self.id = id
        self._style = 'font-size: %spt; font-family: %s; background: %s; color: %s; ' \
                      'margin-top: %spx; margin-bottom: %spx; margin-left: %spx; margin-right: %spx; ' \
                      % (self.font_size, self.font_family, self.bgcolor, self.color, self.margin_top,
                         self.margin_bottom, self.margin_left, self.margin_right)
        self._style_table = 'font-size: %spt; font-family: %s; color: %s;' \
                            ' margin-top: %spx; margin-bottom: %spx; margin-left: %spx; margin-right: %spx;' \
                            % (self.font_size, self.font_family, self.color,
                               self.margin_top, self.margin_bottom, self.margin_left, self.margin_right)

    def update_style(self):
        self._style = 'font-size: %spt ; font-family: %s; background: %s ; color: %s ; ' \
                      'margin-top: %spx; margin-bottom: %spx; margin-left: %spx; margin-right: %spx;' \
                      % (self.font_size, self.font_family, self.bgcolor, self.color, self.margin_top,
                         self.margin_bottom, self.margin_left, self.margin_right)
        self._style_table = 'font-size: %spt; font-family: %s; color: %s ; margin-top: %spx; ' \
                            'margin-bottom: %spx; margin-left: %spx; margin-right: %spx;' \
                            % (self.font_size, self.font_family, self.color, self.margin_top,
                               self.margin_bottom, self.margin_left, self.margin_right)