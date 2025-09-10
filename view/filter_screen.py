from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDoubleSpinBox,
    QCheckBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
import math

from view.widgets import CollapsibleGroupBox, DateFilter
from view import BaseScreen, colors

class FilterScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()
    filter_changed = pyqtSignal(dict) # dict['Date','Category','Amount']

    def __init__(self):
        super().__init__()
        self.checked_categories = []
        self.filter = {'Date': None, 'Category': None, 'Amount': None}
        self.initUI()
        self.update_category_options([f'test{x}' for x in range(8)])

    def initUI(self):
        self.content_layout.setSpacing(25)
        self.add_title(self.content_layout, 'Filter', self.home_clicked.emit, 10)

        # Date row
        self.date_filter = DateFilter()
        self.date_filter.stateChanged.connect(self.on_filter_changed)
        self.date_filter.date_range_changed.connect(self.on_filter_changed)
        self.content_layout.addWidget(self.date_filter)

        # Amount row
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(5)
        self.amount_check_box = QCheckBox('Amount: ')
        self.amount_check_box.setChecked(True)
        self.amount_check_box.stateChanged.connect(self.on_filter_changed)
        row.addWidget(self.amount_check_box)

        self.amount_min = QDoubleSpinBox()
        self.amount_min.setSingleStep(10)
        self.amount_min.setDecimals(2)
        self.amount_min.setMinimum(0)
        self.amount_min.setMaximum(1e5)
        self.amount_min.valueChanged.connect(self.on_filter_changed)
        row.addWidget(self.amount_min)

        label = QLabel(' -- ')
        label.setStyleSheet('font-size: 15px;')
        row.addWidget(label)

        self.amount_max = QDoubleSpinBox()
        self.amount_max.setSingleStep(10)
        self.amount_max.setDecimals(2)
        self.amount_max.setMinimum(0)
        self.amount_max.setMaximum(1e5)
        self.amount_max.valueChanged.connect(self.on_filter_changed)
        row.addWidget(self.amount_max)

        row.addStretch()
        self.content_layout.addLayout(row)

        # Category
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(5)

        left_column = QVBoxLayout()
        left_column.setContentsMargins(0, 0, 0, 0)
        self.category_check_box = QCheckBox('Category: ')
        self.category_check_box.setChecked(True)
        self.category_check_box.stateChanged.connect(self.on_filter_changed)
        left_column.addWidget(self.category_check_box)

        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(20, 0, 0, 0)
        button_layout.addSpacing(10)

        self.all_categories_button = QPushButton('all')
        self.all_categories_button.clicked.connect(lambda: self.check_all_categories()) # this emits false because the button isn't checkable so use a lambda to ignore it
        self.all_categories_button.setFixedSize(50,25)
        self.all_categories_button.setStyleSheet('font-size: 13px;')
        button_layout.addWidget(self.all_categories_button)

        button_layout.addSpacing(10)

        self.no_categories_button = QPushButton('none')
        self.no_categories_button.clicked.connect(lambda: self.check_all_categories(False))
        self.no_categories_button.setFixedSize(50, 25)
        self.no_categories_button.setStyleSheet('font-size: 13px;')
        button_layout.addWidget(self.no_categories_button)

        left_column.addLayout(button_layout)
        left_column.addStretch()
        row.addLayout(left_column)

        self.category_list_buttons: dict[str, QCheckBox] = {}
        self.category_list_layout = QGridLayout()
        self.category_list_layout.setContentsMargins(0, 0, 0, 0)
        self.category_list_layout.setVerticalSpacing(10)
        self.category_list_layout.setHorizontalSpacing(50)
        row.addLayout(self.category_list_layout)

        row.addStretch()
        self.content_layout.addLayout(row)

        self.content_layout.addStretch()

        self.add_continue_cancel_buttons(self.content_layout, self.continue_clicked.emit, self.cancel_clicked.emit)
        keys_functions = [
            ('<return>', 'continue'),
            ('<esc>', 'cancel'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def update_category_options(self, categories: list[str]):
        ratio_nrow_ncol = 2.5
        n = len(categories)
        n_rows = round(math.sqrt(ratio_nrow_ncol * n))
        n_cols = math.ceil(n/n_rows)

        self.category_list_buttons.clear()
        self.clear_layout(self.category_list_layout)
        style = f'''
        QCheckBox::indicator {{
        width: 12px;
        height: 12px;
        }}
        QCheckBox::indicator:checked {{
        background-color: {colors['purple-faded']};
        }}
        '''
        for i, category in enumerate(categories):
            (col, row) = divmod(i, n_rows)
            check_box = QCheckBox(category.replace('&', '&&'))
            check_box.stateChanged.connect(self.on_category_button_toggled)
            check_box.setStyleSheet(style)
            self.category_list_layout.addWidget(check_box, row, col)
            self.category_list_buttons[category] = check_box

        self.category_list_layout.setColumnStretch(n_rows, n_cols)
        self.category_list_layout.setRowStretch(n_rows, n_cols)
        self.check_all_categories()

    def check_all_categories(self, state=True):
        for category, button in self.category_list_buttons.items():
            button.setChecked(state)

    def on_category_button_toggled(self, state):
        self.checked_categories = []
        for category, button in self.category_list_buttons.items():
            if button.isChecked():
                self.checked_categories.append(category)
        self.on_filter_changed()

    def get_amount_range(self):
        """
        Make range negative because expenses are negative
        """
        minimum = self.amount_min.value()
        maximum = self.amount_max.value()

        if minimum == 0 and maximum == 0:
            return None
        if minimum > maximum:
            return None

        return (minimum, maximum)

    def on_filter_changed(self):
        self.filter['Date'] = self.date_filter.date_range if self.date_filter.check_box.isChecked() else None
        self.filter['Amount'] = self.get_amount_range() if self.amount_check_box.isChecked() else None
        self.filter['Category'] = self.checked_categories if self.category_check_box.isChecked() else None
        self.filter_changed.emit(self.filter)
        #print(self.filter) #XXX debug

    def reset(self):
        self.checked_categories = []
        self.filter = {'Date': None, 'Category': None, 'Amount': None}
        self.date_filter.reset()
        self.amount_check_box.setChecked(True)
        self.category_check_box.setChecked(True)
        self.check_all_categories()
