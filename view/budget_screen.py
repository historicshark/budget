from PyQt5.QtWidgets import (
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QWidget,
)
from PyQt5.QtCore import pyqtSignal, Qt

from view import BaseScreen, colors
from view.widgets import DateFilter, ProgressBar

class BudgetScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()
    date_range_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.bars: list[ProgressBar] = []
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

        button_layout = self.add_continue_cancel_buttons(self.content_layout, self.on_continue_clicked, self.on_cancel_clicked)

        self.date_filter = DateFilter(use_check_box=False)
        self.date_filter.disable_options(['last 3 months', 'last 6 months', 'last year', 'range', 'all time'])
        self.date_filter.date_range_changed.connect(self.on_date_range_changed)
        button_layout.addWidget(self.date_filter)

        keys_functions = [
            ('<return>', 'continue'),
            ('<esc>', 'cancel'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def update_budget(self, categories: list[str], amounts_budgeted: list[float], values: list[float], types: list[str]):
        """ values are assumed to be all positive. Don't input spending as negative. """
        self.bars.clear()
        self.clear_layout(self.budget_layout)

        # inputs should not be empty
        if not (categories and amounts_budgeted and values and types):
            print('In budget_screen.py, one or more input to update_budget was empty')
            return

        # all lists should be the same length
        if any(len(l) != len(categories) for l in [categories, amounts_budgeted, values, types]):
            print('In budget_screen.py, not all inputs were the same length')
            return

        if all(v <= 0 for v in values):
            return

        # initialize row for net in/out since QGridLayout doesn't have a way to insert rows
        net_in = 0
        net_out = 0

        label_layout = QVBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.addWidget(QLabel('Total'), alignment=Qt.AlignCenter)
        value_label_net = QLabel(f'{net_out:.2f} / {net_in:.2f}')
        value_label_net.setStyleSheet('font-size: 15px;')
        label_layout.addWidget(value_label_net, alignment=Qt.AlignCenter)

        progress_bar_net = ProgressBar()

        self.bars.append(progress_bar_net)
        self.budget_layout.addLayout(label_layout, 0, 0)
        self.budget_layout.addWidget(progress_bar_net, 0, 1)

        for row, (category, amount_budgeted, value, category_type) in enumerate(zip(categories, amounts_budgeted, values, types)):
            row += 1 # since I already added 1 row for the total

            category_label = QLabel(category)
            value_label = QLabel(f'{value:.2f} / {amount_budgeted:.2f}')
            value_label.setStyleSheet('font-size: 15px;')

            label_layout = QVBoxLayout()
            label_layout.setContentsMargins(0, 0, 0, 0)
            label_layout.addWidget(category_label, alignment=Qt.AlignCenter)
            label_layout.addWidget(value_label, alignment=Qt.AlignCenter)

            self.budget_layout.addLayout(label_layout, row, 0)

            progress_bar = ProgressBar()
            color = colors['green'] if category_type == 'income' else None
            progress_bar.plot(amount_budgeted, value, color)
            self.bars.append(progress_bar)
            self.budget_layout.addWidget(progress_bar, row, 1)

            if category_type == 'income':
                net_in += value
            else:
                net_out += value

        # add values to total bar
        value_label_net.setText(f'{net_out:.2f} / {net_in:.2f}')

        color = colors['green'] if net_out <= net_in else None
        progress_bar_net.plot(net_in, net_out, color)

        # add stretch
        n_rows = row + 1
        self.budget_layout.setColumnStretch(2, 3)
        self.budget_layout.setRowStretch(n_rows, 3)

    def on_date_range_changed(self, date_range: list):
        self.date_range_changed.emit(date_range)

    def on_continue_clicked(self):
        self.continue_clicked.emit()

    def on_cancel_clicked(self):
        self.cancel_clicked.emit()
