from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLayout,
    QLabel,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QAbstractItemView,
    QSpacerItem,
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from decimal import Decimal

from view import BaseScreen, colors
from view.widgets import PlotCategory

class ExpensesScreen(BaseScreen):
    home_clicked = pyqtSignal()
    new_search_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_plot_view = True
        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Expenses', self.home_clicked.emit, 20)

        # Layout with plot and table with summary
        plot_view_layout = QHBoxLayout()
        plot_view_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_view_container = QWidget()
        self.plot_view_container.setLayout(plot_view_layout)

        plot_layout = QVBoxLayout()
        plot_layout.setSpacing(0)
        plot_layout.setContentsMargins(0, 0, 0, 0)
        self.plot = PlotCategory()
        plot_layout.addWidget(self.plot, alignment=Qt.AlignHCenter)
        plot_layout.addStretch()
        plot_view_layout.addLayout(plot_layout)

        summary_table_layout = QVBoxLayout()
        summary_table_layout.setSpacing(0)
        summary_table_layout.setContentsMargins(0, 0, 0, 0)
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(3)
        self.summary_table.setHorizontalHeaderLabels(['Category', 'Amount', '%'])

        header = self.summary_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.summary_table.verticalHeader().setVisible(False)
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.summary_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.summary_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.protect_last_column(self.summary_table)

        summary_table_layout.addWidget(self.summary_table)
        summary_table_layout.addStretch()

        plot_view_layout.addLayout(summary_table_layout)

        self.content_layout.addWidget(self.plot_view_container)

        #self.plot.plot_pie(['test1','test2'], [2,3])

        # Layout with tabs and table by category
        list_view_layout = QHBoxLayout()
        list_view_layout.setContentsMargins(0, 0, 0, 0)
        self.list_view_container = QWidget()
        self.list_view_container.setLayout(list_view_layout)
        self.list_view_container.hide()

        self.tab_widget = QTabWidget()
        list_view_layout.addWidget(self.tab_widget)

        self.content_layout.addWidget(self.list_view_container)

        # Bottom row with button to switch views and new search button
        bottom_row_layout = QHBoxLayout()
        bottom_row_layout.setContentsMargins(0, 0, 0, 0)

        self.switch_view_button = QPushButton('list view')
        self.switch_view_button.setFixedSize(150, 50)
        self.switch_view_button.clicked.connect(self.switch_view)
        self.switch_view_button.setShortcut('v')
        bottom_row_layout.addWidget(self.switch_view_button)

        bottom_row_layout.addStretch()

        new_search_button = QPushButton('new search')
        new_search_button.setFixedSize(150, 50)
        new_search_button.clicked.connect(self.new_search_clicked.emit)
        new_search_button.setShortcut('n')
        new_search_button.setStyleSheet(f'''
                                        QPushButton:hover {{
                                        background-color: {colors['green-faded']};
                                       }}
                                        ''')
        bottom_row_layout.addWidget(new_search_button)

        self.content_layout.addLayout(bottom_row_layout)

        keys_functions = [
            ('v', 'switch view'),
            ('n', 'new search'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def load_widgets(self):
        self.plot.load()

    def update_plot_view(self, categories: list[str], totals: list[Decimal], total_income: Decimal):
        # expenses are negative, so take the negative of them to plot
        # then only keep positive values because negative values can't be plotted
        categories_plot = []
        totals_plot = []
        for c, t in zip(categories, totals):
            if t < 0:
                categories_plot.append(c)
                totals_plot.append(-t)
        self.plot.plot_pie(categories_plot, totals_plot)

        total_all_categories = sum(totals)
        percentages = [total / total_all_categories * 100 for total in totals]

        n_rows = len(categories) + 2
        self.summary_table.setRowCount(n_rows)
        for row, (category, total, percentage) in enumerate(zip(categories, totals, percentages)):
            category_item = QTableWidgetItem(category)
            total_item = QTableWidgetItem(f'{total:.0f}')
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            percentage_item = QTableWidgetItem(f'{percentage:.1f}%')
            self.summary_table.setItem(row, 0, category_item)
            self.summary_table.setItem(row, 1, total_item)
            self.summary_table.setItem(row, 2, percentage_item)

        category_item = QTableWidgetItem('Total')
        total_item = QTableWidgetItem(f'{total_all_categories:.0f}')
        total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        percentage_item = QTableWidgetItem('100%')
        self.summary_table.setItem(n_rows - 2, 0, category_item)
        self.summary_table.setItem(n_rows - 2, 1, total_item)
        self.summary_table.setItem(n_rows - 2, 2, percentage_item)

        category_item = QTableWidgetItem('Income')
        total_item = QTableWidgetItem(f'{total_income:.0f}')
        total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        percentage_item = QTableWidgetItem('---')
        self.summary_table.setItem(n_rows - 1, 0, category_item)
        self.summary_table.setItem(n_rows - 1, 1, total_item)
        self.summary_table.setItem(n_rows - 1, 2, percentage_item)

        for col in range(self.summary_table.columnCount() - 1): # minus 1 since there is a dummy column to protect the scroll bar from overlapping
            item = self.summary_table.item(n_rows - 1, col)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor(colors['purple-faded']))

            item = self.summary_table.item(n_rows - 2, col)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor(colors['blue-faded']))

        # set the table maximum height
        height = self.summary_table.horizontalHeader().height()
        for row in range(self.summary_table.rowCount()):
            height += self.summary_table.rowHeight(row)

        self.summary_table.setFixedHeight(height + 2)

    def update_list_view(self,
                         categories: list[str],
                         dates: dict[str, list[str]],
                         locations: dict[str, list[str]],
                         amounts: dict[str, list[str]],
                         totals: dict[str, Decimal]):
        self.tab_widget.clear()
        for category in categories:
            table = QTableWidget()
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(['Date', 'Location', 'Amount'])
            table.verticalHeader().setVisible(False)
            table.setAlternatingRowColors(True)
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)

            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            assert len(dates[category]) == len(locations[category]) == len(amounts[category]) #XXX debug

            n_rows = len(dates[category]) + 1
            table.setRowCount(n_rows)
            for row, (date, location, amount) in enumerate(zip(dates[category], locations[category], amounts[category])):
                date_item = QTableWidgetItem(date)
                location_item = QTableWidgetItem(location)
                amount_item = QTableWidgetItem(amount)
                amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                table.setItem(row, 0, date_item)
                table.setItem(row, 1, location_item)
                table.setItem(row, 2, amount_item)

            table.setSpan(n_rows - 1, 0, 1, 2)
            total_item = QTableWidgetItem('Total')
            total_amount_item = QTableWidgetItem(f'{totals[category]:.0f}')
            total_amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font = total_item.font()
            font.setBold(True)
            total_item.setFont(font)
            total_item.setBackground(QColor(colors['purple-faded']))
            total_amount_item.setFont(font)
            total_amount_item.setBackground(QColor(colors['purple-faded']))
            table.setItem(n_rows - 1, 0, total_item)
            table.setItem(n_rows - 1, 2, total_amount_item)

            # set table maximum height
            height = table.verticalHeader().length() + table.horizontalHeader().height()
            table.setMaximumHeight(height + 2)

            self.tab_widget.addTab(table, category.replace('&', '&&'))

    def switch_view(self):
        if self.is_plot_view:
            self.plot_view_container.hide()
            self.list_view_container.show()
            self.switch_view_button.setText('plot view')
            self.switch_view_button.setShortcut('v')
        else:
            self.list_view_container.hide()
            self.plot_view_container.show()
            self.switch_view_button.setText('list view')
            self.switch_view_button.setShortcut('v')
        self.is_plot_view = not self.is_plot_view

