from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QPushButton,
    QShortcut,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from global_variables import COLORS, SCREENS
from fcn.import_categorize import Importer


class CategorizeScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget, importer: Importer):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.importer = importer

        self.initUI()
    
    def initUI(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15,0,15,0)

        # title
        title_layout = QHBoxLayout()
        label_title = QLabel('Import')
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        home_button = QPushButton('Home')
        home_button.clicked.connect(self.go_home)
        home_button.setFixedSize(70, 30)
        home_button.setShortcut('h')

        home_button.setStyleSheet(f'''
                                   QPushButton {{
                                   font-family: Monaco;
                                   font-size: 14px;
                                   background-color: {COLORS['gray']};
                                   color: {COLORS['bg']};
                                 }}

                                 QPushButton:hover {{
                                   background-color: {COLORS['aqua']};
                                   color: {COLORS['fg']};
                                }}
                                  ''')

        label_title.setStyleSheet(f'''
                                  font-family: Monaco;
                                  font-size: 25px;
                                  color: {COLORS['fg']};
                                  margin: 10px;
                                  ''')
        
        title_layout.addWidget(home_button)
        title_layout.addWidget(label_title)
        title_layout.addSpacing(70)
        self.layout.addLayout(title_layout)
        self.layout.addSpacing(50)

        # Two columns showing transaction and category options
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        


    def display_transaction(self):
        pass

    def continue_button_pressed(self):
        print('continue')
    
    def cancel_button_pressed(self):
        self.stacked_widget.setCurrentIndex(SCREENS.IMPORT)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(SCREENS.HOME)