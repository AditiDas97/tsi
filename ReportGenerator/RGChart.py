try:
    from .RGHeadlines import Drawing, VerticalBarChart, Pie, HorizontalLineChart, LinePlot, mm, cm, A4, renderPM, \
        math, colors, os
    from .RGImage import RGImage
except ImportError:
    from RGHeadlines import Drawing, VerticalBarChart, Pie, HorizontalLineChart, LinePlot, mm, cm, A4, renderPM, \
        math, colors, os
    from RGImage import RGImage


class RGChart:

    def __init__(self, name=str('temp'), type=str('BChart'), data=[], axis_names=[], width=400, height=200):
        self.name_graph = name
        self.type_graph = type
        self.data_graph = data
        self.width = width
        self.height = height
        self.drawing = Drawing(width + 200, height + 100)
        if self.type_graph == "BChart":  # data_graph is formed as a list of lists(matrix), values = numbers
            if len(self.data_graph) <= 1:
                tmp_list = list()
                for i in range(len(self.data_graph[0])):
                        tmp_list.append(0)
                self.data_graph.append(tmp_list)
            sort_data = list()
            min = 999999
            max = 0
            for i in self.data_graph:
                sort_data.append(sorted(i))
            for i in sort_data:
                for j in i:
                    if j >= max:
                        max = j
                    elif j <= min:
                        min = j
            mean_value = int((math.fabs(max) + math.fabs(min)) / 10)
            if mean_value <= 0:
                mean_value = 1
            newChart = VerticalBarChart()
            newChart.x = 50
            newChart.y = 50
            newChart.groupSpacing = 5
            newChart.barSpacing = 5
            newChart.height = self.height
            newChart.width = self.width
            newChart.data = self.data_graph
            newChart.strokeColor = colors.black
            newChart.valueAxis.valueMin = min - 1
            newChart.valueAxis.valueMax = max + 1
            newChart.valueAxis.valueStep = mean_value
            newChart.categoryAxis.categoryNames = axis_names
        elif self.type_graph == "LChart":  # data_graph is formed as a list of lists(matrix), values = numbers
            if len(self.data_graph) <= 1:
                tmp_list = list()
                for i in range(len(self.data_graph[0])):
                        tmp_list.append(0)
                self.data_graph.append(tmp_list)
            sort_data = list()
            min = 999999
            max = 0
            for i in self.data_graph:
                sort_data.append(sorted(i))
            for i in sort_data:
                for j in i:
                    if j >= max:
                        max = j
                    elif j <= min:
                        min = j
            mean_value = int((math.fabs(max) + math.fabs(min))/ 10)
            if mean_value <= 0:
                mean_value = 1
            newChart = HorizontalLineChart()
            newChart.x = 50
            newChart.y = 50
            newChart.height = self.height
            newChart.width = self.width
            newChart.data = self.data_graph
            newChart.categoryAxis.categoryNames = axis_names
            newChart.valueAxis.valueMin = min - 1
            newChart.valueAxis.valueMax = max + 1
            newChart.valueAxis.valueStep = mean_value
        elif self.type_graph == "LPlot":  # dataChart is formed as a list of lists containing the coordinates of points (x, y)
            min_x = 999999
            min_y = 999999
            max_x = 0
            max_y = 0
            if len(self.data_graph) <= 1:
                tmp_list = list()
                for i in range(len(self.data_graph[0])):
                    tmp_list.append([0, 0])
                self.data_graph.append(tmp_list)
            for i in range(len(self.data_graph)):
                for list_points in self.data_graph[i]:
                    if list_points[0] >= max_x:
                        max_x = list_points[0]
                    elif list_points[0] <= min_x:
                        min_x = list_points[0]
                    if list_points[1] >= max_y:
                        max_y = list_points[1]
                    elif list_points[1] <= min_y:
                        min_y = list_points[1]
            list_Y_axis_names = list()
            list_X_axis_names = list()
            list_Y_axis_names.append(min_y - 1)
            list_X_axis_names.append(min_x - 1)
            if min_x < 0:
                mean_value_x = max_x - min_x
            else:
                mean_value_x = max_x + min_x
            i = 0
            while list_X_axis_names[i] < max_x:
                list_X_axis_names.append(int(mean_value_x/len(self.data_graph[0])) + list_X_axis_names[i])
                i += 1

            if min_y < 0:
                mean_value_y = max_y - min_y
            else:
                mean_value_y = max_y + min_y
            i = 0
            while list_Y_axis_names[i] < max_x:
                list_Y_axis_names.append(int(mean_value_y/len(self.data_graph[0])) + list_Y_axis_names[i])
                i += 1
            newChart = LinePlot()
            newChart.x = 50
            newChart.y = 50
            newChart.height = self.height
            newChart.width = self.width
            newChart.data = self.data_graph
            newChart.strokeColor = colors.black
            newChart.xValueAxis.valueMin = min_x - 1
            newChart.xValueAxis.valueMax = max_x + 1
            newChart.xValueAxis.valueSteps = list_X_axis_names
            newChart.yValueAxis.valueMin = min_y - 1
            newChart.yValueAxis.valueMax = max_y + 1
            newChart.yValueAxis.valueSteps = list_Y_axis_names
        elif self.type_graph == "PChart":  # dataChart formed as a list of values (numbers)
            newChart = Pie()
            newChart.x = 50
            newChart.y = 50
            newChart.slices.strokeWidth = 1
            newChart.slices.fontSize = 12
            newChart.width = self.width
            newChart.height = self.height + 50
            newChart.data = self.data_graph
            newChart.labels = axis_names
            newChart.sideLabels = 1
        self.drawing.add(newChart)
        local_path = os.getcwd()
        renderPM.drawToFile(self.drawing, local_path+ "\\" + self.name_graph + ".png", 'PNG')
        self.obj = RGImage(local_path + "\\" + self.name_graph + ".png", width=self.width, height=self.height)

    def to_text(self):
        return self.name_graph + " " + self.type_graph

    def to_json(self):
        return {"type": "graph", "typeChart": self.type_graph, "nameChart": self.name_graph,
                'width': self.width, 'height': self.height,
                'alt': "NAN", 'id': self.name_graph, 'align': "center"}

    def to_pdf(self, pdf):
        self.obj.to_pdf(pdf)

    def to_html(self):
        return "<img class='all_foto' src='" + self.name_graph + "' width='" + str(self.width) + "' height='" + \
               str(self.height) + "'alt='NAN' id='" + self.name_graph + "' onclick = 'openImageWindow(this.src);' />"
