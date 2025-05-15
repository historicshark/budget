from PyQt5.QtWidgets import (
    QMainWindow,
    QStackedWidget,
)

from PyQt5.QtGui import QPalette, QColor

import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Budget Program')
        self.setGeometry(100, 100, 800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        with open('view/colors.json', 'r') as f:
            colors = json.load(f)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(colors['bg']))
        self.setPalette(palette)
