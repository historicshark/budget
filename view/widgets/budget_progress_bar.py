from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from view import colors

class BudgetProgressBar(QWidget):
    """ This keeps track of whether it has been loaded """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loaded = False
        self.plot_later = None

    def load(self):
        if not self.loaded:
            import matplotlib
            matplotlib.use('Qt5Agg', force=True)
            self.figure = Figure(figsize=(8,0.4), facecolor='none')
            self.ax = self.figure.subplots(1, 1)
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setStyleSheet('background-color: transparent;')
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.addWidget(self.canvas)
            self.setLayout(self.layout)
            self.loaded = True

            if self.plot_later:
                self.plot_bar(**self.plot_later)

    def plot_bar(self, maximum: float, value: float, color=None):
        """ Specify color, otherwise it is green if value < maximum and red if value > maximum """
        if self.loaded:
            self.ax.clear()
            if color is None:
                color = colors['green'] if value < maximum else colors['red']
            self.ax.barh('1', maximum, height=1.0, color='none', edgecolor=colors['fg'])
            if value > 0:
                self.ax.barh('1', value-0.2, left=0.2, height=0.6, color=color, edgecolor='none')
            self.ax.axis('off')
            self.ax.axis('tight')
            self.canvas.draw()
            self.plot_later = None
        else:
            self.plot_later = {'maximum': maximum, 'value': value, 'color': color}
