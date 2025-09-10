from PyQt5.QtWidgets import (
    QMainWindow,
    QStackedWidget,
)

from PyQt5.QtGui import QPalette, QColor

from model import get_asset_path

import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Budget Program')
        self.setGeometry(560, 150, 800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        with open(get_asset_path('assets/colors.json'), 'r') as f:
            colors = json.load(f)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(colors['bg']))
        self.setPalette(palette)

