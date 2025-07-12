import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from view import colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PlotCategory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure(figsize=(4.5,3), facecolor='none')
        self.ax = self.figure.subplots(1, 1)
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.99, bottom=0.01)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: transparent;")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

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

