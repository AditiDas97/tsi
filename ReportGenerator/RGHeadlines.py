import json
import copy
import time
import re
import os
import math
import shutil
from datetime import timedelta
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics import renderPM
from reportlab.lib import colors
from reportlab.lib.pagesizes import A1, A2, A3, A4, A5, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

dict_format_page = {
    'portrait':
        {
            'A1': A1,
            'A2': A2,
            'A3': A3,
            'A4': A4,
            'A5': A5
        },
    'landscape':
        {
            'A1': landscape(A1),
            'A2': landscape(A2),
            'A3': landscape(A3),
            'A4': landscape(A4),
            'A5': landscape(A5)
        }
}


def sort_col(i):
    return i[1]


def find_max_len_str(temp_list):
    result = len(temp_list[0])
    for i in temp_list:
        if len(i) > result:
            result = len(i)
    return result
