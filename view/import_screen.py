from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QPushButton,
    QShortcut,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QFileDialog,
)

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence

from view.base_screen import BaseScreen
from view.default_style_sheet import colors

class ImportScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()
    open_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.file = ''
        self.file_exists = False
        self.account = ''

        self.initUI()

    def initUI(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15,0,15,0)
        
        self.add_title(self.layout, 'Import', self.home_clicked.emit)

        # import button
        row_layout = QHBoxLayout()
        open_button = QPushButton('Open...')
        open_button.setFixedSize(150, 50)
        open_button.clicked.connect(self.open_file_dialog)
        open_button.setShortcut('o')

        self.import_label = QLabel('Choose a file to import')
        self.import_label.setStyleSheet(f'''
                            font-size: 14px;
                            color: {colors['gray']};
                            ''')

        row_layout.addWidget(open_button)
        row_layout.addSpacing(10)
        row_layout.addWidget(self.import_label)
        row_layout.addStretch()

        self.layout.addLayout(row_layout)

        self.layout.addSpacing(25)

        # credit/debit radio buttons - only shown if a csv file is imported
        account_type_layout = QVBoxLayout()

        self.label_description = QLabel('Choose credit or debit')

        self.credit_button = QRadioButton('credit')
        self.credit_button.setShortcut('c')
        self.credit_button.toggled.connect(self.credit_button_toggled)

        self.debit_button = QRadioButton('debit')
        self.debit_button.setShortcut('d')
        self.debit_button.toggled.connect(self.debit_button_toggled)

        account_type_layout.addWidget(self.label_description)
        account_type_layout.addWidget(self.credit_button)
        account_type_layout.addWidget(self.debit_button)

        self.set_account_buttons_visibility(False)

        self.layout.addLayout(account_type_layout)

        # continue/cancel
        self.layout.addStretch()
        self.add_continue_cancel_buttons(self.layout, self.continue_clicked.emit, self.cancel_clicked.emit)

        # footer
        keys_functions = [('o', 'open file'),
                          ('c', 'credit'),
                          ('d', 'debit'),
                          ('<return>', 'continue'),
                          ('<esc>', 'cancel'),
                         ]
        # self.layout.addStretch()
        self.add_footer(self.layout, keys_functions)

        self.setLayout(self.layout)
        

    def credit_button_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            self.account = 'credit'
        self.check_activate_continue_button()

    def debit_button_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            self.account = 'debit'
        self.check_activate_continue_button()
    
    def set_account_buttons_visibility(self, is_visible: bool):
        self.label_description.setVisible(is_visible)
        self.credit_button.setVisible(is_visible)
        self.debit_button.setVisible(is_visible)

    def open_file_dialog(self):
        self.file, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Statement Files (*.ofx *.qbo *.qfx *.csv)')
        if self.file:
            if Path(self.file).exists():
                self.import_label.setText(f'{self.file}')
                self.import_label.setStyleSheet(f'''
                                color: {colors['fg']};
                                ''')
                self.file_exists = True
            else:
                self.import_label.setText('Error!')
                self.import_label.setStyleSheet(f'''
                                color: {colors['red']};
                                ''')
        self.check_activate_account_buttons()
        self.check_activate_continue_button()
    
    def check_activate_account_buttons(self):
        if self.file_exists and self.file.lower().endswith('.csv'):
            self.set_account_buttons_visibility(True)
        else:
            self.set_account_buttons_visibility(False)

    def check_activate_continue_button(self):
        if self.file_exists and (self.file.lower().endswith(('.ofx','.qbo','.qfx')) or (self.account and self.file.lower().endswith('.csv'))):
            self.continue_button.setEnabled(True)
            self.continue_button.setStyleSheet(f'''
                               QPushButton {{
                               font-family: Monaco;
                               font-size: 18px;
                               background-color: {colors['gray']};
                               color: {colors['bg']};
                             }}

                             QPushButton:hover {{
                               background-color: {colors['purple']};
                               color: {colors['fg']};
                            }}
                                           ''')
        else:
            self.continue_button.setDisabled(True)
            self.continue_button.setStyleSheet(f'''
                               QPushButton {{
                               font-family: Monaco;
                               font-size: 18px;
                               background-color: {colors['bg1']};
                               color: {colors['gray']};
                             }}

                             QPushButton:hover {{
                               background-color: {colors['purple']};
                               color: {colors['fg']};
                            }}
                                           ''')

    def continue_button_pressed(self):
        self.importer.set_file(self.file)
        self.importer.import_file(self.account)
        self.stacked_widget.setCurrentIndex(SCREENS.CATEGORIZE)
    
    def cancel_button_pressed(self):
        self.file = ''
        self.file_exists = False
        self.import_label.setText('Choose a file to import')
        self.set_account_buttons_visibility(False)
        self.stacked_widget.setCurrentIndex(SCREENS.HOME)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(SCREENS.HOME)
