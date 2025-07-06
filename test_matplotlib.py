import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        
        # Add canvas to layout
        layout.addWidget(self.canvas)
        
        # Add button to generate new plot
        self.plot_button = QPushButton("Generate Plot")
        self.plot_button.clicked.connect(self.plot_data)
        layout.addWidget(self.plot_button)
        
        self.setLayout(layout)
        self.plot_data()  # Initial plot
    
    def plot_data(self):
        # Clear previous plot
        self.figure.clear()
        
        # Create subplot
        ax = self.figure.add_subplot(111)
        
        # Generate sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x) + np.random.normal(0, 0.1, 100)
        
        # Plot data
        ax.plot(x, y, 'b-', linewidth=2, label='Sin wave with noise')
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_title('Sample Plot')
        ax.legend()
        ax.grid(True)
        
        # Refresh canvas
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Matplotlib Example")
        self.setGeometry(100, 100, 800, 600)
        
        # Set central widget
        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
