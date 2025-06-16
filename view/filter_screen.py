from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QFormLayout,
)
from PyQt5.QtCore import pyqtSignal

from view.widgets import CollapsibleGroupBox, DateFilter
from view.base_screen import BaseScreen
from view.default_style_sheet import colors

class FilterScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.base_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.base_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setContentsMargins(15,0,15,0)
        self.base_layout.addLayout(self.content_layout)

        self.add_title(self.content_layout, 'Filter', self.home_clicked.emit)
        self.content_layout.addSpacing(10)

        self.date_filter = DateFilter()
        self.content_layout.addWidget(self.date_filter)

        self.content_layout.addStretch()
        keys_functions = [('test', 'test'),
                         ]
        self.add_footer(self.base_layout, keys_functions)

        self.setLayout(self.base_layout)

