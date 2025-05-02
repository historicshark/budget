import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
)

from PyQt5.QtGui import QPalette, QColor

from global_variables import COLORS
from ui.home_screen import HomeScreen
from ui.import_screen import ImportScreen
from ui.categorize_screen import CategorizeScreen
from fcn.import_categorize import Importer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Budget Program')
        self.setGeometry(100, 100, 800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(COLORS['bg']))
        self.setPalette(palette)

        # logic classes
        importer = Importer()

        # ui classes
        self.home_screen = HomeScreen(self.stack)
        self.import_screen = ImportScreen(self.stack, importer)
        self.categorize_screen = CategorizeScreen(self.stack, importer)

        # self.stack.addWidget(self.home_screen)
        # self.stack.addWidget(self.import_screen)
        self.stack.addWidget(self.categorize_screen)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

