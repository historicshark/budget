import sys

from PyQt5.QtWidgets import QApplication

from controller.main_controller import MainController
from view.default_style_sheet import default_style_sheet

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(default_style_sheet)
    main_controller = MainController()
    main_controller.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
