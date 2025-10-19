from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QWidget,
)
from PyQt5.QtCore import pyqtSignal, Qt

from view import BaseScreen, colors
from view.widgets import BudgetProgressBar

class BudgetScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.bars: list[BudgetProgressBar] = []
        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Monthly Budget', self.home_clicked.emit, 10)

        # Scroll area with a grid list of categories and progress bars
        scroll_area_widget = QWidget()
        self.budget_layout = QGridLayout()
        self.budget_layout.setHorizontalSpacing(30)
        self.budget_layout.setVerticalSpacing(20)
        scroll_area_widget.setLayout(self.budget_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(scroll_area_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content_layout.addWidget(self.scroll_area)

    def update_budget(self, categories: list[str], amounts_budgeted: list[float], values: list[float], types: list[str]):
        self.bars.clear()
        self.clear_layout(self.budget_layout)
        for row, (category, amount_budgeted, value, category_type) in enumerate(zip(categories, amounts_budgeted, values, types)):
            category_label = QLabel(category)
            value_label = QLabel(f'{value:.2f} / {amount_budgeted:.2f}')
            value_label.setStyleSheet('font-size: 15px;')

            label_layout = QVBoxLayout()
            label_layout.setContentsMargins(0, 0, 0, 0)
            label_layout.addWidget(category_label, alignment=Qt.AlignCenter)
            label_layout.addWidget(value_label, alignment=Qt.AlignCenter)

            self.budget_layout.addLayout(label_layout, row, 0)

            progress_bar = BudgetProgressBar()
            color = colors['green'] if category_type == 'income' else None
            progress_bar.plot_bar(amount_budgeted, value, color)
            self.bars.append(progress_bar)
            self.budget_layout.addWidget(progress_bar, row, 1)

        n_rows = row + 1
        self.budget_layout.setColumnStretch(2, 3)
        self.budget_layout.setRowStretch(n_rows, 3)

    def load_bars(self):
        for bar in self.bars:
            bar.load()
