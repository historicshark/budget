from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QColor, QFont
from view import colors

class PlotCategory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loaded = False

    def load(self):
        if not self.loaded:
            import matplotlib
            matplotlib.use('Qt5Agg', force=True)
            self.figure = Figure(figsize=(5,3), facecolor='none')
            self.ax = self.figure.subplots(1, 1)
            self.figure.subplots_adjust(left=0.1, right=0.9, top=0.99, bottom=0.01)
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setStyleSheet("background-color: transparent;")
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.addWidget(self.canvas)
            self.setLayout(self.layout)
            self.loaded = True

    def plot_pie(self, categories, totals):
        self.ax.clear()
        self.ax.set_prop_cycle(color=[colors['purple-faded'], colors['blue-faded'], colors['green-faded'], colors['aqua-faded'], colors['red-faded'], colors['yellow-faded']])
        self.ax.pie(totals,
                    labels=categories,
                    textprops={'color': colors['fg'],
                               'fontsize': 9,
                              'fontname': 'Monaco'},
                    wedgeprops={'linewidth': 1.5, 'edgecolor': colors['bg']},
                   )
        self.canvas.draw()

class PieChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.legend().hide()

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.chart_view)
        self.setLayout(self.layout)
        self.setMinimumSize(450, 400)

        self.color_cycle = [colors['purple-faded'], colors['blue-faded'], colors['green-faded'], colors['aqua-faded'], colors['red-faded'], colors['yellow-faded']]
        self.n_colors = len(self.color_cycle)

    def plot(self, categories, totals):
        self.chart.removeAllSeries()

        categories_sorted, totals_sorted = zip(*sorted(zip(categories, totals), key=lambda c_t: c_t[1]))

        # now sort alternating big and small totals to reduce label overlap
        categories = []
        totals = []
        for i in range(len(totals_sorted)):
            if i % 2 == 0:
                categories.append(categories_sorted[i // 2])
                totals.append(totals_sorted[i // 2])
            else:
                categories.append(categories_sorted[-(i+1) // 2])
                totals.append(totals_sorted[-(i+1) // 2])

        series = QPieSeries()
        for i, (category, total) in enumerate(zip(categories, totals)):
            color = QColor(self.color_cycle[i % self.n_colors])

            pie_slice = QPieSlice(category, total)
            pie_slice.setColor(color)
            pie_slice.setLabelVisible(True)
            pie_slice.setLabelColor(QColor(colors['fg']))
            pie_slice.setLabelFont(QFont('Monaco', 10))
            pie_slice.setBorderColor(color)

            series.append(pie_slice)

        start = 115
        series.setPieStartAngle(start)
        series.setPieEndAngle(start + 360)
        self.chart.addSeries(series)
