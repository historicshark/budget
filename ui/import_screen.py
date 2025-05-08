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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from global_variables import COLORS, SCREENS
from fcn.import_categorize import Importer


class ImportScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget, importer: Importer):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.file = ''
        self.file_exists = False
        self.account = ''
        self.importer = importer
        self.initUI()

    def initUI(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15,0,15,0)
        
        # title
        title_layout = QHBoxLayout()
        label_title = QLabel('Import')
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        home_button = QPushButton('Home')
        home_button.clicked.connect(self.go_home)
        home_button.setFixedSize(70, 30)

        home_button.setStyleSheet(f'''
                                   QPushButton {{
                                   font-family: Monaco;
                                   font-size: 14px;
                                   background-color: {COLORS['gray']};
                                   color: {COLORS['bg']};
                                 }}

                                 QPushButton:hover {{
                                   background-color: {COLORS['aqua']};
                                   color: {COLORS['fg']};
                                }}
                                  ''')

        label_title.setStyleSheet(f'''
                                  font-family: Monaco;
                                  font-size: 25px;
                                  color: {COLORS['fg']};
                                  margin: 10px;
                                  ''')
        
        title_layout.addWidget(home_button)
        title_layout.addWidget(label_title)
        title_layout.addSpacing(70)
        self.layout.addLayout(title_layout)
        self.layout.addSpacing(50)

        # import button
        row_layout = QHBoxLayout()
        import_button = QPushButton('Open...')
        import_button.setFixedSize(150, 50)
        import_button.clicked.connect(self.open_file_dialog)
        import_button.setShortcut('o')

        self.import_label = QLabel('Choose a file to import')

        import_button.setStyleSheet(f'''
                             QPushButton {{
                               font-family: Monaco;
                               font-size: 18px;
                               background-color: {COLORS['gray']};
                               color: {COLORS['bg']};
                             }}

                             QPushButton:hover {{
                               background-color: {COLORS['purple']};
                               color: {COLORS['fg']};
                            }}
                             ''')

        self.import_label.setStyleSheet(f'''
                            font-family: Monaco;
                            font-size: 14px;
                            color: {COLORS['gray']};
                            ''')

        row_layout.addWidget(import_button)
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

        self.label_description.setStyleSheet(f'''
                                        font-family: Monaco;
                                        font-size: 18px;
                                        color: {COLORS['fg']};
                                        ''')
        
        button_format = f'''
            font-family: Monaco;
            font-size: 16px;
            color: {COLORS['fg']};
            '''
        self.credit_button.setStyleSheet(button_format)
        self.debit_button.setStyleSheet(button_format)

        account_type_layout.addWidget(self.label_description)
        account_type_layout.addWidget(self.credit_button)
        account_type_layout.addWidget(self.debit_button)

        self.set_account_buttons_visibility(False)

        self.layout.addLayout(account_type_layout)

        # continue/cancel
        self.layout.addStretch()

        continue_button_layout = QHBoxLayout()
        self.continue_button = QPushButton('Continue')
        self.continue_button.setFixedSize(150, 50)
        self.continue_button.clicked.connect(self.continue_button_pressed)
        self.continue_button.setDisabled(True)
        continue_shortcut = QShortcut(QKeySequence('Return'), self)
        continue_shortcut.activated.connect(self.continue_button.click)
        
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setFixedSize(150, 50)
        self.cancel_button.clicked.connect(self.cancel_button_pressed)
        cancel_shortcut = QShortcut(QKeySequence('Escape'), self)
        cancel_shortcut.activated.connect(self.cancel_button.click)

        self.continue_button.setStyleSheet(f'''
                               QPushButton {{
                               font-family: Monaco;
                               font-size: 18px;
                               background-color: {COLORS['bg1']};
                               color: {COLORS['gray']};
                             }}

                             QPushButton:hover {{
                               background-color: {COLORS['purple']};
                               color: {COLORS['fg']};
                            }}
                                           ''')
        
        self.cancel_button.setStyleSheet(f'''
                               QPushButton {{
                               font-family: Monaco;
                               font-size: 18px;
                               background-color: {COLORS['gray']};
                               color: {COLORS['bg']};
                             }}

                             QPushButton:hover {{
                               background-color: {COLORS['orange']};
                               color: {COLORS['fg']};
                            }}
                                           ''')
        continue_button_layout.addWidget(self.continue_button)
        continue_button_layout.addWidget(self.cancel_button)
        continue_button_layout.addStretch()
        self.layout.addLayout(continue_button_layout)

        # footer
        keys_functions = [('o', 'open file'),
                          ('c', 'credit'),
                          ('d', 'debit'),
                          ('<return>', 'continue'),
                          ('<esc>', 'cancel'),
                         ]
        # self.layout.addStretch()
        footer = QLabel(' • '.join([f'{function}: {key}' for key, function in keys_functions]))
        footer.setStyleSheet(f'''
                             QLabel {{
                             background-color: {COLORS['fg']};
                             color: {COLORS['bg']};
                             font-family: Monaco;
                             font-size: 14px;
                             padding: 3px;
                            }}
                             ''')
        self.layout.addWidget(footer)

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
                                font-family: Monaco;
                                font-size: 14px;
                                color: {COLORS['fg']};
                                ''')
                self.file_exists = True
            else:
                self.import_label.setText('Error!')
                self.import_label.setStyleSheet(f'''
                                font-family: Monaco;
                                font-size: 14px;
                                color: {COLORS['red']};
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
                               background-color: {COLORS['gray']};
                               color: {COLORS['bg']};
                             }}

                             QPushButton:hover {{
                               background-color: {COLORS['purple']};
                               color: {COLORS['fg']};
                            }}
                                           ''')
        else:
            self.continue_button.setDisabled(True)
            self.continue_button.setStyleSheet(f'''
                               QPushButton {{
                               font-family: Monaco;
                               font-size: 18px;
                               background-color: {COLORS['bg1']};
                               color: {COLORS['gray']};
                             }}

                             QPushButton:hover {{
                               background-color: {COLORS['purple']};
                               color: {COLORS['fg']};
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
