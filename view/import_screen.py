from pathlib import Path

from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QFileDialog,
)

from PyQt5.QtCore import pyqtSignal

from view.base_screen import BaseScreen
from view.default_style_sheet import colors

class ImportScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()
    file_chosen = pyqtSignal(str)
    account_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.initUI()
        self.set_continue_button_enabled(False)
        self.set_account_buttons_visibility(False)

    def initUI(self):
        self.base_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.base_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setContentsMargins(15,0,15,0)
        self.base_layout.addLayout(self.content_layout)
        
        self.add_title(self.content_layout, 'Import', self.home_clicked.emit)

        # import button
        row_layout = QHBoxLayout()
        open_button = QPushButton('Open...')
        open_button.setFixedSize(150, 50)
        open_button.clicked.connect(self.open_file_dialog)
        open_button.setShortcut('o')

        self.import_label = QLabel('Choose a file to import') #XXX long filename make the window bigger
        self.import_label.setStyleSheet(f'''
                            font-size: 14px;
                            color: {colors['gray']};
                            ''')
        self.import_label.setWordWrap(True)

        row_layout.addWidget(open_button)
        row_layout.addSpacing(10)
        row_layout.addWidget(self.import_label)

        self.content_layout.addLayout(row_layout)

        self.content_layout.addSpacing(25)

        # credit/debit radio buttons - only shown if a csv file is imported
        account_type_layout = QVBoxLayout()

        self.label_description = QLabel('Choose credit or debit')

        self.credit_button = QRadioButton('credit')
        self.credit_button.setShortcut('c')
        self.credit_button.toggled.connect(self.account_button_toggled)

        self.debit_button = QRadioButton('debit')
        self.debit_button.setShortcut('d')
        self.debit_button.toggled.connect(self.account_button_toggled)

        account_type_layout.addWidget(self.label_description)
        account_type_layout.addWidget(self.credit_button)
        account_type_layout.addWidget(self.debit_button)

        self.content_layout.addLayout(account_type_layout)

        # continue/cancel
        self.content_layout.addStretch()
        self.add_continue_cancel_buttons(self.content_layout, self.continue_clicked.emit, self.cancel_clicked.emit)

        # footer
        keys_functions = [('o', 'open file'),
                          ('<return>', 'continue'),
                          ('<esc>', 'cancel'),
                         ]
        # self.content_layout.addStretch()
        self.add_footer(self.base_layout, keys_functions)

        self.setLayout(self.base_layout)

    def account_button_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            self.account_clicked.emit(sender.text())
    
    def set_account_buttons_visibility(self, is_visible: bool):
        self.label_description.setVisible(is_visible)
        self.credit_button.setVisible(is_visible)
        self.debit_button.setVisible(is_visible)
        if is_visible:
            keys_functions = [('o', 'open file'),
                              ('c', 'credit'),
                              ('d', 'debit'),
                              ('<return>', 'continue'),
                              ('<esc>', 'cancel'),
                             ]
        else:
            keys_functions = [('o', 'open file'),
                              ('<return>', 'continue'),
                              ('<esc>', 'cancel'),
                             ]
        self.update_footer(keys_functions)

    def open_file_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Statement Files (*.ofx *.qbo *.qfx *.csv)')
        if file:
            if Path(file).exists():
                self.import_label.setText(f'{file}')
                self.import_label.setStyleSheet(f'''
                                font-size: 14px;
                                color: {colors['fg']};
                                ''')
            else:
                self.import_label.setText('Error!')
                self.import_label.setStyleSheet(f'''
                                font-size: 14px;
                                color: {colors['red']};
                                ''')
            self.file_chosen.emit(file)
    
    def set_continue_button_enabled(self, enable: bool):
        self.continue_button.setEnabled(enable)

    def reset(self):
        """
        Resets file labels, disables continue, and removes account buttons
        """
        self.import_label.setText('Choose a file to import')
        self.import_label.setStyleSheet(f'''
                            font-size: 14px;
                            color: {colors['gray']};
                            ''')
        self.set_account_buttons_visibility(False)
        self.set_continue_button_enabled(False)

