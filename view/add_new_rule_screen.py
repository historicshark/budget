from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QFormLayout,
    QLineEdit,
)
from PyQt5.QtCore import pyqtSignal
from view import BaseScreen, colors

class AddNewRuleScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal(str)
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Import', self.home_clicked.emit)

        # Two columns showing transaction and add new rule
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

        self.add_continue_cancel_buttons(left_layout, self.on_continue_clicked, self.cancel_clicked.emit)
        self.continue_button.setText('Add rule')
        self.cancel_button.setText('No')

        # right layout
        self.instruction_label = QLabel('Add new rule?')
        self.instruction_label.setStyleSheet(label_style)
        right_layout.addWidget(self.instruction_label)

        right_layout.addSpacing(10)

        self.text_box = QLineEdit('Enter rule here')
        right_layout.addWidget(self.text_box)
        right_layout.addStretch()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.content_layout.addLayout(main_layout)

        # footer
        keys_functions = [
            ('<return>', 'yes'),
            ('<esc>', 'no'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def display_transaction(self, record: dict[str, str], index, length):
        self.index_label.setText(f'Categorize transaction {index+1} of {length}:')
        self.location_label.setText(f'Transaction: {record["Location"]}')
        self.date_label.setText(f'Date: {record["Date"]}')
        self.amount_label.setText(f'Amount: ${record["Amount"]}')
        self.text_box.setText(f'{record["Location"]}')

    def on_continue_clicked(self):
        self.continue_clicked.emit(self.text_box.text())

    def set_text_new_rule(self):
        self.text_box.setFocus()
        self.instruction_label.setText('Add new rule?')
        self.continue_button.setText('Add Rule')
        self.cancel_button.setText('No')

    def set_text_new_category(self):
        self.text_box.setFocus()
        self.instruction_label.setText('Add new category?')
        self.continue_button.setText('Continue')
        self.cancel_button.setText('Cancel')
