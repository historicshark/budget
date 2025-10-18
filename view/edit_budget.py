from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QDoubleSpinBox,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from view import BaseScreen, colors

class EditBudgetScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.categories: list[str] = []
        self.amounts: list[QDoubleSpinBox] = []
        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Edit Monthly Budget', self.home_clicked.emit, 20)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addLayout(layout)

        # scroll area with categories and amounts
        list_widget = QWidget()
        self.list_layout = QGridLayout()
        self.list_layout.setHorizontalSpacing(30)
        self.list_layout.setVerticalSpacing(10)
        list_widget.setLayout(self.list_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(list_widget)
        layout.addWidget(self.scroll_area)

        # Layout with summary table and buttons
        summary_table_layout = QVBoxLayout()
        summary_table_layout.setSpacing(0)
        summary_table_layout.setContentsMargins(0, 0, 0, 0)
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(['a', 'b'])
        self.summary_table.horizontalHeader().setVisible(False)

        self.summary_table.verticalHeader().setVisible(False)
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.summary_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.summary_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.protect_last_column(self.summary_table)

        summary_table_layout.addWidget(self.summary_table, alignment=Qt.AlignCenter)
        summary_table_layout.addStretch()

        button_layout = self.add_continue_cancel_buttons(summary_table_layout, self.on_continue_clicked, self.on_cancel_clicked, add_stretch='both')
        layout.addLayout(summary_table_layout)

        keys_functions = [
            ('<return>', 'continue'),
            ('<esc>', 'cancel'),
        ]
        self.add_footer(self.base_layout, keys_functions)

        #self.update_category_options([f'test{x}' for x in range(5)],
        #                             [10*x for x in range(5)])
        #self.update_summary_table(['income', 'expense', 'savings', 'net'],
        #                          [6000.0, 5400.0, 200.0, 400.0])

    def update_category_options(self, categories: list[str], amounts: list[float]):
        for row, (category, amount) in enumerate(zip(categories, amounts)):
            label = QLabel(category.replace('&', '&&'))

            box = QDoubleSpinBox()
            box.setSingleStep(10)
            box.setDecimals(2)
            box.setMinimum(0)
            box.setMaximum(1e5)
            box.setValue(amount)

            self.list_layout.addWidget(label, row, 0)
            self.list_layout.addWidget(box, row, 1)

        n_rows = row + 1
        self.list_layout.setColumnStretch(2, 3)
        self.list_layout.setRowStretch(n_rows, 3)

    def update_summary_table(self, category_types: list[str], amounts: list[float]):
        """ category_types and amounts should contain the net/total in the last element """
        n_rows = len(category_types)
        self.summary_table.setRowCount(n_rows)
        for row, (category_type, amount) in enumerate(zip(category_types, amounts)):
            category_type_item = QTableWidgetItem(category_type)
            amount_item = QTableWidgetItem(f'{amount:.2f}')
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.summary_table.setItem(row, 0, category_type_item)
            self.summary_table.setItem(row, 1, amount_item)

        width = 0
        for col in range(self.summary_table.columnCount() - 1): # minus 1 since there is a dummy column to protect the scroll bar from overlapping
            item = self.summary_table.item(n_rows - 1, col)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor(colors['purple-faded']))

            width += self.summary_table.columnWidth(col)

        # set the table size
        height = self.summary_table.verticalHeader().length() + self.summary_table.horizontalHeader().height()
        self.summary_table.setFixedHeight(height + 2)
        self.summary_table.setMaximumWidth(width + 2)

    def on_continue_clicked(self):
        self.continue_clicked.emit()

    def on_cancel_clicked(self):
        self.cancel_clicked.emit()
