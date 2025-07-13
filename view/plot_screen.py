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
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor

from decimal import Decimal

from view import BaseScreen, colors
from view.widgets import PlotCategory, ComboBoxFix

class PlotScreen(BaseScreen):
    home_clicked = pyqtSignal()
    new_search_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.show_menu_options = ['both', 'expenses', 'income']
        self.initUI()

    def initUI(self):
        self.base_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(20)
        self.base_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setContentsMargins(15,0,15,0)
        self.base_layout.addLayout(self.content_layout)

        self.add_title(self.content_layout, 'Plot', self.home_clicked.emit)

        # Layout with plot and table with summary
        plot_view_layout = QHBoxLayout()
        plot_view_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_view_container = QWidget()
        self.plot_view_container.setLayout(plot_view_layout)

        plot_layout = QVBoxLayout()
        plot_layout.setSpacing(0)
        plot_layout.setContentsMargins(0, 0, 0, 0)
        self.plot = PlotCategory()
        plot_label = QLabel('Expenses')
        plot_layout.addWidget(plot_label, alignment=Qt.AlignHCenter)
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
        self.summary_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.summary_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        plot_view_layout.addWidget(self.summary_table)

        plot_view_layout.addStretch()

        self.content_layout.addWidget(self.plot_view_container)

        self.plot.plot_pie(['test1','test2'], [2,3])

        # Bottom row with drop down menu and button for new search
        bottom_row_layout = QHBoxLayout()

        new_search_button = QPushButton('New Search')
        new_search_button.setFixedSize(150, 50)
        new_search_button.clicked.connect(self.new_search_clicked.emit)
        new_search_button.setStyleSheet(f'''
                                        QPushButton:hover {{
                                        background-color: {colors['green-faded']};
                                       }}
                                        ''')
        bottom_row_layout.addWidget(new_search_button)

        self.content_layout.addLayout(bottom_row_layout)

        keys_functions = [('test', 'test'),
                         ]
        self.content_layout.addStretch()
        self.add_footer(self.base_layout, keys_functions)
        self.setLayout(self.base_layout)

    def update_plot_view(self, categories: list[str], totals: list[Decimal]):
        self.plot.plot_pie(categories, totals)

        total_all_categories = sum(totals)
        percentages = [total / total_all_categories * 100 for total in totals]

        n_rows = len(categories) + 1
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
        self.summary_table.setItem(n_rows - 1, 0, category_item)
        self.summary_table.setItem(n_rows - 1, 1, total_item)
        self.summary_table.setItem(n_rows - 1, 2, percentage_item)

        for col in range(self.summary_table.columnCount()):
            item = self.summary_table.item(n_rows - 1, col)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor(colors['purple-faded']))

        # set the table maximum height
        height = self.summary_table.verticalHeader().length() + self.summary_table.horizontalHeader().height()
        self.summary_table.setMaximumHeight(height + 2)

