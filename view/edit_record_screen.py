from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDoubleSpinBox,
    QLineEdit,
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate

import datetime

from view import BaseScreen, colors
from view.widgets import DateEditFix, ComboBoxFix

class EditRecordScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.date = None
        self.location = None
        self.category = None
        self.amount = None

        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Edit', self.home_clicked.emit)

        def add_row(name, widget):
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(5)

            label = QLabel(f'{name}:')

            row.addWidget(label)
            row.addWidget(widget)
            row.addStretch()
            self.content_layout.addLayout(row)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(50)

        label = QLabel('Date:')
        self.date_edit = DateEditFix()
        self.date_edit.setFixedWidth(120)
        self.date_edit.dateChanged.connect(self.on_date_changed)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.date_edit, 0, 1)

        label = QLabel('Location:')
        self.location_edit = QLineEdit()
        self.location_edit.textChanged.connect(self.on_location_changed)
        layout.addWidget(label, 1, 0)
        layout.addWidget(self.location_edit, 1, 1)

        label = QLabel('Category:')
        self.category_edit = ComboBoxFix()
        self.category_edit.addItems(['test1', 'test2'])
        self.category_edit.setFixedWidth(150)
        self.category_edit.view().setMinimumWidth(self.category_edit.width() + 6)
        self.category_edit.currentTextChanged.connect(self.on_category_changed)
        layout.addWidget(label, 2, 0)
        layout.addWidget(self.category_edit, 2, 1)

        label = QLabel('Amount:')
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setSingleStep(10)
        self.amount_edit.setDecimals(2)
        self.amount_edit.setMinimum(-1e5)
        self.amount_edit.setMaximum(1e5)
        self.amount_edit.setMaximumWidth(200)
        self.amount_edit.valueChanged.connect(self.on_amount_changed)
        layout.addWidget(label, 3, 0)
        layout.addWidget(self.amount_edit, 3, 1)

        layout.setRowStretch(1, 2)

        self.content_layout.addLayout(layout)

        self.content_layout.addStretch()
        self.add_continue_cancel_buttons(self.content_layout, self.continue_clicked.emit, self.cancel_clicked.emit)

        keys_functions = [
            ('test','test'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def on_date_changed(self, date):
        print(date)

    def on_location_changed(self, text):
        print(text)

    def on_category_changed(self, text):
        print(text)

    def on_amount_changed(self, value):
        print(value)
