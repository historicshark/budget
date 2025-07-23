from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
)
from PyQt5.QtCore import pyqtSignal, Qt

from view import BaseScreen, colors
from view.widgets import ComboBoxFix

class ListScreen(BaseScreen):
    home_clicked = pyqtSignal()
    new_search_clicked = pyqtSignal()
    edit_selected_clicked = pyqtSignal()
    sort_by_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'List', self.home_clicked.emit, 20)

        # table layout
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['', 'Date', 'Location', 'Category', 'Amount'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.cellDoubleClicked.connect(self.on_table_cell_double_clicked)
        self.table.itemChanged.connect(self.on_table_item_changed)

        self.content_layout.addWidget(self.table) # adding alignment makes the table small

        # bottom row layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(30)

        # Select all / none
        select_layout = QVBoxLayout()
        select_layout.setContentsMargins(0, 0, 0, 0)
        select_layout.setSpacing(5)
        label = QLabel('select')
        label.setStyleSheet('font-size: 14px;')
        select_layout.addWidget(label, alignment=(Qt.AlignTop | Qt.AlignHCenter))

        all_none_layout = QHBoxLayout()
        all_none_layout.setContentsMargins(0, 0, 0, 0)
        all_none_layout.setSpacing(20)
        select_all_button = QPushButton('all')
        select_all_button.setFixedSize(50, 30)
        select_all_button.setStyleSheet('font-size: 14px;')
        select_all_button.clicked.connect(self.on_select_all_clicked)
        all_none_layout.addWidget(select_all_button)

        select_none_button = QPushButton('none')
        select_none_button.setFixedSize(50, 30)
        select_none_button.setStyleSheet('font-size: 14px;')
        select_none_button.clicked.connect(self.on_select_none_clicked)
        all_none_layout.addWidget(select_none_button)

        select_layout.addLayout(all_none_layout)

        button_layout.addLayout(select_layout)
        button_layout.addStretch()

        # edit selected
        edit_selected_button = QPushButton('edit selected')
        edit_selected_button.setFixedSize(150, 50)
        edit_selected_button.clicked.connect(self.on_edit_selected_clicked)
        button_layout.addWidget(edit_selected_button)
        button_layout.addStretch()

        # sort by
        sort_by_layout = QHBoxLayout()
        sort_by_layout.setContentsMargins(0, 0, 0, 0)
        sort_by_layout.setSpacing(10)

        label = QLabel('sort by:')
        label.setStyleSheet('font-size: 14px;')
        drop_down = ComboBoxFix()
        drop_down.addItems(['date', 'location', 'category', 'amount'])
        drop_down.setFixedWidth(100)
        drop_down.view().setMinimumWidth(drop_down.width() + 6)
        drop_down.setCurrentIndex(0)
        drop_down.currentTextChanged.connect(self.on_sort_by_changed)
        drop_down.setStyleSheet('font-size: 14px;')

        sort_by_layout.addWidget(label, alignment=(Qt.AlignLeft | Qt.AlignVCenter))
        sort_by_layout.addWidget(drop_down, alignment=(Qt.AlignLeft | Qt.AlignVCenter))
        button_layout.addLayout(sort_by_layout)
        button_layout.addStretch()

        # new search
        new_search_button = QPushButton('new search')
        new_search_button.setFixedSize(150, 50)
        new_search_button.clicked.connect(self.new_search_clicked.emit)
        new_search_button.setShortcut('n')
        new_search_button.setStyleSheet(f'''
                                        QPushButton:hover {{
                                        background-color: {colors['green-faded']};
                                       }}
                                        ''')
        button_layout.addWidget(new_search_button)
        self.content_layout.addLayout(button_layout)

        keys_functions = [
            ('test', 'test'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def update_table(self, records: list):
        self.table.clearContents()
        n_rows = len(records)
        self.table.setRowCount(n_rows)

        for row, record in enumerate(records):
            print(f'creating row {row}')
            check_box_item = QTableWidgetItem()
            check_box_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            check_box_item.setCheckState(Qt.Unchecked)

            date_item = QTableWidgetItem(record['Date'])
            location_item = QTableWidgetItem(record['Location'])
            category_item = QTableWidgetItem(record['Category'])
            amount_item = QTableWidgetItem(f'{record['Amount']} ')
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.table.setItem(row, 0, check_box_item)
            self.table.setItem(row, 1, date_item)
            self.table.setItem(row, 2, location_item)
            self.table.setItem(row, 3, category_item)
            self.table.setItem(row, 4, amount_item)

        height = self.table.verticalHeader().length() + self.table.horizontalHeader().height()
        self.table.setMaximumHeight(height + 2)

    def on_table_cell_double_clicked(self, row, col):
        print(f'cell clicked: {row}, {col}')

    def on_table_item_changed(self, item: QTableWidgetItem):
        print(f'{item.row()}, {item.column()}')

    def on_select_all_clicked(self):
        print('select all')

    def on_select_none_clicked(self):
        print('select none')

    def on_edit_selected_clicked(self):
        print('edit selected')

    def on_sort_by_changed(self, text):
        self.sort_by_changed.emit(text)
