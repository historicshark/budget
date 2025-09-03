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
from model import Record

class ListScreen(BaseScreen):
    home_clicked = pyqtSignal()
    new_search_clicked = pyqtSignal()
    edit_clicked = pyqtSignal(list)
    delete_clicked = pyqtSignal(list)
    sort_by_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.indices_selected = []
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
        select_all_button.setShortcut('Ctrl+A')
        all_none_layout.addWidget(select_all_button)

        select_none_button = QPushButton('none')
        select_none_button.setFixedSize(50, 30)
        select_none_button.setStyleSheet('font-size: 14px;')
        select_none_button.clicked.connect(self.on_select_none_clicked)
        select_none_button.setShortcut('Ctrl+N')
        all_none_layout.addWidget(select_none_button)

        select_layout.addLayout(all_none_layout)

        button_layout.addLayout(select_layout)
        button_layout.addStretch()

        # edit selected
        edit_button = QPushButton('edit')
        edit_button.setFixedSize(100, 50)
        edit_button.clicked.connect(self.on_edit_clicked)
        edit_button.setShortcut('e')
        button_layout.addWidget(edit_button)
        button_layout.addStretch()

        # delete selected
        delete_button = QPushButton('delete')
        delete_button.setFixedSize(100, 50)
        delete_button.clicked.connect(self.on_delete_clicked)
        delete_button.setShortcut('d')
        button_layout.addWidget(delete_button)
        button_layout.addStretch()

        # sort by
        sort_by_layout = QHBoxLayout()
        sort_by_layout.setContentsMargins(0, 0, 0, 0)
        sort_by_layout.setSpacing(10)

        label = QLabel('sort by:')
        label.setStyleSheet('font-size: 14px;')
        self.drop_down = ComboBoxFix()
        self.drop_down.addItems(['date', 'location', 'category', 'amount'])
        self.drop_down.setFixedWidth(100)
        self.drop_down.view().setMinimumWidth(self.drop_down.width() + 6)
        self.drop_down.setCurrentIndex(0)
        self.drop_down.currentTextChanged.connect(self.on_sort_by_changed)
        self.drop_down.setStyleSheet('font-size: 14px;')

        sort_by_layout.addWidget(label, alignment=(Qt.AlignLeft | Qt.AlignVCenter))
        sort_by_layout.addWidget(self.drop_down, alignment=(Qt.AlignLeft | Qt.AlignVCenter))
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
            ('<cmd>+A/N', 'select all/none'),
            ('e', 'edit'),
            ('d', 'delete'),
            ('n', 'new search'),
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

            date_item = QTableWidgetItem(record.date_str())
            location_item = QTableWidgetItem(record.location)
            category_item = QTableWidgetItem(record.category)
            amount_item = QTableWidgetItem(f'{record.amount_str()} ')
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.table.setItem(row, 0, check_box_item)
            self.table.setItem(row, 1, date_item)
            self.table.setItem(row, 2, location_item)
            self.table.setItem(row, 3, category_item)
            self.table.setItem(row, 4, amount_item)

        height = self.table.verticalHeader().length() + self.table.horizontalHeader().height()
        self.table.setMaximumHeight(height + 2)
        self.get_selected_indices()

    def set_row_check_state(self, row, state):
        assert row >= 0 and row < self.table.rowCount()
        item = self.table.item(row, 0)
        item.setCheckState(Qt.Checked if state else Qt.Unchecked)

    def get_selected_indices(self):
        self.indices_selected.clear()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item.checkState() == Qt.Checked:
                self.indices_selected.append(row)

    def on_table_cell_double_clicked(self, row, col):
        """ Only edit the record that is clicked """
        self.on_select_none_clicked()
        self.set_row_check_state(row, True)
        self.on_edit_clicked()

    def on_table_item_changed(self, item: QTableWidgetItem):
        row = item.row()
        if item.checkState() == Qt.Checked and row not in self.indices_selected:
            self.indices_selected.append(row)
        elif item.checkState() == Qt.Unchecked and row in self.indices_selected:
            self.indices_selected.remove(row)
        self.indices_selected.sort()
        print(f'{item.row()}, {item.column()}; selected: {self.indices_selected}')

    def on_select_all_clicked(self):
        for row in range(self.table.rowCount()):
            self.set_row_check_state(row, True)

    def on_select_none_clicked(self):
        for row in range(self.table.rowCount()):
            self.set_row_check_state(row, False)

    def on_edit_clicked(self):
        self.get_selected_indices()
        print(self.indices_selected)
        self.edit_clicked.emit(self.indices_selected)

    def on_delete_clicked(self):
        self.get_selected_indices()
        print(self.indices_selected)
        self.delete_clicked.emit(self.indices_selected)

    def on_sort_by_changed(self, text):
        self.sort_by_changed.emit(text)
