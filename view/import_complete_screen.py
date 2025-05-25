from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import pyqtSignal

from view.base_screen import BaseScreen

class ImportCompleteScreen(BaseScreen):
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

        self.add_title(self.content_layout, 'Import', self.home_clicked.emit)

        self.content_layout.addSpacing(50)

        label = QLabel('Import Complete!')
        self.content_layout.addWidget(label)

        self.content_layout.addStretch()
        self.add_continue_cancel_buttons(self.content_layout, self.continue_clicked.emit, self.cancel_clicked.emit)

        keys_functions = [('<return>', 'continue'),
                          ('<esc>', 'cancel'),
                         ]
        self.add_footer(self.base_layout, keys_functions)

        self.setLayout(self.base_layout)
