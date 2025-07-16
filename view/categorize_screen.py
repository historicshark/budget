from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QFormLayout,
)
from PyQt5.QtCore import pyqtSignal

from string import ascii_lowercase

from view import BaseScreen, colors
from model import Categories

class CategorizeScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()
    skip_clicked = pyqtSignal()
    category_chosen = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.buttons: dict[str, QRadioButton] = {}
        self.button_layout = QFormLayout()
        self.button_layout.setContentsMargins(0,0,0,0)

        self.initUI()
        self.set_continue_button_enabled(False)

    def initUI(self):
        self.add_title(self.content_layout, 'Import', self.home_clicked.emit)

        # Two columns showing transaction and category options
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Left column - current transaction being categorized and the continue and cancel buttons
        left_layout.addSpacing(10)

        self.index_label = QLabel('Categorize transaction X of X')
        self.location_label = QLabel('Transaction: ')
        self.date_label = QLabel('Date: ')
        self.amount_label = QLabel('Amount: $')

        left_layout.addWidget(self.index_label)
        left_layout.addWidget(self.location_label)
        left_layout.addWidget(self.date_label)
        left_layout.addWidget(self.amount_label)

        label_style = f'''
                      font-size: 18px;
                      margin: 3px;
                      '''
        self.index_label.setStyleSheet(label_style)
        self.location_label.setStyleSheet(label_style)
        self.date_label.setStyleSheet(label_style)
        self.amount_label.setStyleSheet(label_style)
        self.location_label.setWordWrap(True)

        left_layout.addStretch()

        continue_cancel_layout = self.add_continue_cancel_buttons(left_layout, self.continue_clicked.emit, self.cancel_clicked.emit, add_stretch=False)
        skip_button = QPushButton('Skip')
        skip_button.setFixedSize(150, 50)
        skip_button.clicked.connect(self.skip_clicked.emit)
        skip_button.setShortcut('Ctrl+S')
        skip_button.setStyleSheet(f'QPushButton:hover {{ background-color: {colors["yellow-faded"]}; }}')
        continue_cancel_layout.addSpacing(20)
        continue_cancel_layout.addWidget(skip_button)
        continue_cancel_layout.addStretch()

        # right layout - options
        instruction_label = QLabel('Choose a category:')
        instruction_label.setStyleSheet(label_style)
        right_layout.addWidget(instruction_label)
        right_layout.addSpacing(10)
        right_layout.addLayout(self.button_layout)
        right_layout.addStretch()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.content_layout.addLayout(main_layout)

        # footer
        keys_functions = [
            ('<return>', 'continue'),
            ('<esc>', 'cancel'),
            ('<cmd>+S', 'skip'),
            ('<key>', 'select category'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def display_transaction(self, record: dict[str, str], index, length):
        self.index_label.setText(f'Categorize transaction {index+1} of {length}:')
        self.location_label.setText(f'Transaction: {record["Location"]}')
        self.date_label.setText(f'Date: {record["Date"]}')
        self.amount_label.setText(f'Amount: ${record["Amount"]}')

    def update_category_buttons(self, categories: list[str]):
        self.clear_layout(self.button_layout)
        self.buttons.clear()
        style = f'''
                font-size: 16px;
                '''
        for key, category in zip(ascii_lowercase, categories):
            key_label = QLabel(f'({key})')
            button = QRadioButton(category.replace('&', '&&'))
            button.setShortcut(key)
            button.toggled.connect(self.category_button_toggled)
            self.buttons[category] = button

            key_label.setStyleSheet(style)
            button.setStyleSheet(style)
            self.button_layout.addRow(key_label, button)
        
        key_label = QLabel(3*' ')
        button = QRadioButton('New Category')
        button.toggled.connect(self.category_button_toggled)
        self.buttons['New Category'] = button
        key_label.setStyleSheet(style)
        button.setStyleSheet(style)
        self.button_layout.addRow(key_label, button)

    def guess_category(self, guessed_category: str):
        if guessed_category in self.buttons.keys():
            self.buttons[guessed_category].setChecked(True)
        else:
            print('Warning: guessed category {guessed_category} not in available buttons on screen') #XXX debug

    def category_button_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            tmp = sender.text().replace('&&','&')
            print(f'in categorize screen, category is {tmp}') #XXX debug
            self.category_chosen.emit(tmp)

    def set_continue_button_enabled(self, enable: bool):
        self.continue_button.setEnabled(enable)
