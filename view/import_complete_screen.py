from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import pyqtSignal

from view import BaseScreen

class ImportCompleteScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Import', self.home_clicked.emit)

        self.content_layout.addSpacing(50)

        label = QLabel('Import Complete!')
        self.content_layout.addWidget(label)

        self.content_layout.addStretch()
        self.add_continue_cancel_buttons(self.content_layout, self.continue_clicked.emit, self.cancel_clicked.emit)

        keys_functions = [
            ('<return>', 'continue'),
            ('<esc>', 'cancel'),
        ]
        self.add_footer(self.base_layout, keys_functions)
