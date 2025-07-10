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
)
from PyQt5.QtCore import pyqtSignal, Qt

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
        plot_layout = QHBoxLayout()
        self.plot_container = QWidget()
        self.plot_container.setLayout(plot_layout)

        expenses_layout = QVBoxLayout()
        expenses_layout.setSpacing(0)
        self.expenses_plot = PlotCategory()
        expenses_label = QLabel('Expenses')
        expenses_layout.addWidget(expenses_label, alignment=Qt.AlignHCenter)
        expenses_layout.addWidget(self.expenses_plot, alignment=Qt.AlignHCenter)
        expenses_layout.addStretch()
        plot_layout.addLayout(expenses_layout)

        summary_table_layout = QVBoxLayout()
        summary_table_layout.setSpacing(0)
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(3)
        self.summary_table.setHorizontalHeaderLabels(['Category', 'Amount', '%'])

        plot_layout.addStretch()

        self.content_layout.addLayout(plot_layout)

        self.expenses_plot.plot_pie(['test1','test2'], [2,3])
        self.income_plot.plot_pie(['Plot','test2'], [2,1])

        # Bottom row with drop down menu and button for new search
        bottom_row_layout = QHBoxLayout()

        label = QLabel('Show:')
        self.show_menu = ComboBoxFix()
        self.show_menu.addItems(self.show_menu_options)
        self.show_menu.setFixedWidth(150)
        self.show_menu.view().setMinimumWidth(156)
        self.show_menu.currentTextChanged.connect(self.on_show_menu_item_selected)
        self.show_menu.setCurrentIndex(1)

        bottom_row_layout.addSpacing(200)
        bottom_row_layout.addWidget(label)
        bottom_row_layout.addWidget(self.show_menu)
        
        bottom_row_layout.addStretch()
        
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

    def on_show_menu_item_selected(self, option):
        match option:
            case 'both':
                self.expenses_container.show()
                self.income_container.show()
            case 'expenses':
                self.expenses_container.show()
                self.income_container.hide()
            case 'income':
                self.expenses_container.hide()
                self.income_container.show()

    def update_plot_view(self, categories: list[str], totals: list[Decimal]):
        self.expenses_plot.plot_pie(categories, totals)

        total_all_categories = sum(totals)
        percentages = ['{0:.1f}%'.format(total / total_all_categories) for total in totals]

