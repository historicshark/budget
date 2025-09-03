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

from view import BaseScreen, colors
from view.widgets import DateEditFix, ComboBoxFix
from model import Record

class AddNewCategoryScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal(str)
    cancel_clicked = pyqtSignal()
    new_category_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.reset()

    def initUI(self):
        self.add_title(self.content_layout, 'Add New Category', self.home_clicked.emit)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(50)

        self.date_label = QLabel('Date:')
        self.date_edit = DateEditFix()
        self.date_edit.setFixedWidth(120)
        self.date_edit.setDisabled(True)
        layout.addWidget(self.date_label, 0, 0)
        layout.addWidget(self.date_edit, 0, 1)

        self.location_label = QLabel('Location:')
        self.location_edit = QLineEdit()
        self.location_edit.setFixedWidth(500)
        self.location_edit.setStyleSheet('font-size: 14px;')
        self.location_edit.setDisabled(True)
        layout.addWidget(self.location_label, 1, 0)
        layout.addWidget(self.location_edit, 1, 1)

        self.category_label = QLabel('Category:')
        self.category_edit = QLineEdit()
        self.category_edit.setFixedWidth(400)
        self.category_edit.setStyleSheet('font-size: 14px;')
        layout.addWidget(self.category_label, 2, 0)
        layout.addWidget(self.category_edit, 2, 1)

        self.amount_label = QLabel('Amount:')
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setSingleStep(10)
        self.amount_edit.setDecimals(2)
        self.amount_edit.setMinimum(-1e5)
        self.amount_edit.setMaximum(1e5)
        self.amount_edit.setMaximumWidth(200)
        self.amount_edit.setDisabled(True)
        layout.addWidget(self.amount_label, 3, 0)
        layout.addWidget(self.amount_edit, 3, 1)

        layout.setColumnStretch(2, 100)

        self.content_layout.addLayout(layout)

        self.content_layout.addStretch()
        self.add_continue_cancel_buttons(self.content_layout, self.on_continue_clicked, self.on_cancel_clicked)

        keys_functions = [
            ('<return>','continue'),
            ('<esc>', 'cancel'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def display_record(self, record: Record):
        self.date_edit.setDate(QDate().fromString(str(record.date_str()), Qt.ISODate))
        self.location_edit.setText(record.location)
        self.amount_edit.setValue(record.amount)

    def on_continue_clicked(self):
        new_category = self.category_edit.currentText()
        self.reset()
        self.continue_clicked.emit(new_category)

    def on_cancel_clicked(self):
        self.reset()
        self.cancel_clicked.emit()

    def reset(self):
        self.date_edit.set_date_today()
        self.location_edit.setText('')
        self.category_edit.setText('New Category')
        self.amount_edit.setValue(0.0)
