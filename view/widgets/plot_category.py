from model.file_handling import is_app_frozen

def setup_matplotlib_for_pyinstaller():
    """Optimize matplotlib loading for PyInstaller environment"""

    # Check if we're running in a PyInstaller bundle
    if is_app_frozen():
        # We're in a PyInstaller bundle - apply optimizations

        # Set matplotlib backend immediately
        import matplotlib
        matplotlib.use('Qt5Agg', force=True)

        # Configure minimal rcParams to avoid expensive discovery
        matplotlib.rcParams.update({
            'font.family': ['Monaco'],  # Your specific font only
            'font.size': 9,
            'figure.max_open_warning': 0,
            'axes.formatter.useoffset': False,
            'interactive': False,  # Disable interactive features
            'toolbar': 'None',     # Disable toolbar
        })

        # Monkey patch font manager to use minimal font set
        from matplotlib import font_manager

        # Override the expensive font discovery with a minimal set
        def fast_findfont(prop, **kwargs):
            return 'Monaco'  # Always return your preferred font

        # Apply the fast font finder (be careful - this is aggressive)
        font_manager.fontManager.findfont = fast_findfont

        print("Matplotlib optimized for PyInstaller")
        return True
    else:
        # Running in development - use normal matplotlib
        import matplotlib
        matplotlib.use('Qt5Agg')
        return False

#setup_matplotlib_for_pyinstaller()

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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

