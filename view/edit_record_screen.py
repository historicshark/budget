from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDoubleSpinBox,
    QLineEdit,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate

import datetime

from view import BaseScreen, colors
from view.widgets import DateEditFix, ComboBoxFix
from model import Record

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
        self.category_options = ['test1','test2']

        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Edit', self.home_clicked.emit)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(50)

        self.date_label = QLabel('Date:')
        self.date_edit = DateEditFix()
        self.date_edit.setFixedWidth(120)
        self.date_edit.dateChanged.connect(self.on_date_changed)
        layout.addWidget(self.date_label, 0, 0)
        layout.addWidget(self.date_edit, 0, 1)

        self.location_label = QLabel('Location:')
        self.location_edit = QLineEdit()
        self.location_edit.setFixedWidth(500)
        self.location_edit.setStyleSheet('font-size: 14px;')
        self.location_edit.textChanged.connect(self.on_location_changed)
        layout.addWidget(self.location_label, 1, 0)
        layout.addWidget(self.location_edit, 1, 1)

        self.category_label = QLabel('Category:')
        self.category_edit = ComboBoxFix()
        self.category_edit.addItems(self.category_options)
        self.category_edit.setFixedWidth(150)
        self.category_edit.view().setMinimumWidth(self.category_edit.width() + 6)
        self.category_edit.currentTextChanged.connect(self.on_category_changed)
        layout.addWidget(self.category_label, 2, 0)
        layout.addWidget(self.category_edit, 2, 1)

        self.amount_label = QLabel('Amount:')
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setSingleStep(10)
        self.amount_edit.setDecimals(2)
        self.amount_edit.setMinimum(-1e5)
        self.amount_edit.setMaximum(1e5)
        self.amount_edit.setMaximumWidth(200)
        self.amount_edit.valueChanged.connect(self.on_amount_changed)
        layout.addWidget(self.amount_label, 3, 0)
        layout.addWidget(self.amount_edit, 3, 1)

        layout.setColumnStretch(2, 100)

        self.content_layout.addLayout(layout)

        self.content_layout.addStretch()
        self.add_continue_cancel_buttons(self.content_layout, self.continue_clicked.emit, self.cancel_clicked.emit)

        keys_functions = [
            ('test','test'),
        ]
        self.add_footer(self.base_layout, keys_functions)

        #self.add_debug_borders()
        self.enable_category_only(True)
        self.display_record(Record('2025-08-30','test','test1','20'))

    def set_category_options(self, categories):
        self.category_edit.clear()
        self.category_edit.addItems(categories)

    def display_record(self, record: Record):
        self.date_edit.setDate(QDate().fromString(str(record.date_str()), Qt.ISODate))
        self.location_edit.setText(record.location)
        self.amount_edit.setValue(record.amount)

        category_index = self.category_edit.findText(record.category)
        if category_index < 0:
            raise IndexError(f'{record} has a category that is not listed!')
        self.category_edit.setCurrentIndex(category_index)

    def on_date_changed(self, date):
        print(date)

    def on_location_changed(self, text):
        print(text)

    def on_category_changed(self, text):
        print(text)

    def on_amount_changed(self, value):
        print(value)

    def enable_category_only(self, enable: bool):
        enable = not enable
        self.date_label.setEnabled(enable)
        self.location_label.setEnabled(enable)
        self.amount_label.setEnabled(enable)
        self.date_edit.setEnabled(enable)
        self.location_edit.setEnabled(enable)
        self.amount_edit.setEnabled(enable)
