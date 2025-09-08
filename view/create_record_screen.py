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

class CreateRecordScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal(Record)
    cancel_clicked = pyqtSignal()
    new_category_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.reset()

    def initUI(self):
        self.add_title(self.content_layout, 'Create Record', self.home_clicked.emit)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(50)

        self.date_label = QLabel('Date:')
        self.date_edit = DateEditFix()
        self.date_edit.setFixedWidth(120)
        layout.addWidget(self.date_label, 0, 0)
        layout.addWidget(self.date_edit, 0, 1)

        self.location_label = QLabel('Location:')
        self.location_edit = QLineEdit()
        self.location_edit.setFixedWidth(500)
        self.location_edit.setStyleSheet('font-size: 14px;')
        layout.addWidget(self.location_label, 1, 0)
        layout.addWidget(self.location_edit, 1, 1)

        self.category_label = QLabel('Category:')
        self.category_edit = ComboBoxFix()
        self.category_edit.addItems(['test1','test2'])
        self.category_edit.setFixedWidth(200)
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

    def update_category_options(self, categories):
        self.category_edit.clear()
        self.category_edit.addItems(categories)
        self.category_edit.addItem('New Category')

    def set_category(self, category: str):
        category_index = self.category_edit.findText(category)
        if category_index < 0:
            raise IndexError(f'category {category} does not exist')
        self.category_edit.setCurrentIndex(category_index)

    def display_record(self, record: Record):
        self.date_edit.setDate(QDate().fromString(str(record.date_str()), Qt.ISODate))
        self.location_edit.setText(record.location)
        self.amount_edit.setValue(record.amount)
        self.set_category(record.category)

    def on_category_changed(self, text):
        if text == 'New Category':
            self.new_category_clicked.emit()

    def get_record(self) -> Record:
        new_date = self.date_edit.date().toPyDate()
        new_location = self.location_edit.text()
        new_category = self.category_edit.currentText()
        new_amount = self.amount_edit.value()
        return Record(new_date, new_location, new_category, new_amount)

    def on_continue_clicked(self):
        record = self.get_record()
        self.reset()
        self.continue_clicked.emit(record)

    def on_cancel_clicked(self):
        self.reset()
        self.cancel_clicked.emit()

    def reset(self):
        self.date_edit.set_date_today()
        self.location_edit.setText('')
        self.category_edit.setCurrentIndex(0)
        self.amount_edit.setValue(0.0)
