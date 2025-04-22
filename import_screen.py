from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
)

from PyQt5.QtCore import Qt

from global_variables import COLORS


class ImportScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10,10,10,10)
        
        # Screen title
        label_title = QLabel('Import')
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label_title.setStyleSheet(f'''
                                  font-family: Monaco;
                                  font-size: 25px;
                                  color: {COLORS['fg']};
                                  margin: 10px;
                                  ''')
        self.layout.addWidget(label_title)

        # import button
        row_layout = QHBoxLayout()
        import_button = QPushButton('Open...')
        import_button.setFixedSize(150, 50)
        import_button.clicked.connect(self.open_file_dialog)
        import_button.setShortcut('o')

        self.import_label = QLabel('Choose a csv file to import')

        import_button.setStyleSheet(f'''
                             QPushButton {{
                               font-family: Monaco;
                               font-size: 18px;
                               background-color: {COLORS['gray']};
                               color: {COLORS['bg']};
                             }}

                             QPushButton:hover {{
                               background-color: {COLORS['purple']};
                               color: {COLORS['fg']};
                            }}
                             ''')

        self.import_label.setStyleSheet(f'''
                            font-family: Monaco;
                            font-size: 18px;
                            color: {COLORS['orange']};
                            ''')

        row_layout.addWidget(import_button)
        row_layout.addWidget(self.import_label)
        row_layout.addStretch()


    def open_file_dialog(self):
        pass
