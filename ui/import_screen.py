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
from fcn.import_csv import import_credit, import_debit


class ImportScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.filename = ''
        self.file_exists = False
        self.account = ''
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
        home_button.setShortcut('h')

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

        self.import_label = QLabel('Choose a csv file to import')

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

        # credit/debit radio buttons
        account_type_layout = QVBoxLayout()

        label_description = QLabel('Choose credit or debit')

        credit_button = QRadioButton('credit')
        credit_button.setShortcut('c')
        credit_button.toggled.connect(self.credit_button_toggled)

        debit_button = QRadioButton('debit')
        debit_button.setShortcut('d')
        debit_button.toggled.connect(self.debit_button_toggled)

        label_description.setStyleSheet(f'''
                                        font-family: Monaco;
                                        font-size: 18px;
                                        color: {COLORS['fg']};
                                        ''')
        
        button_format = f'''
            font-family: Monaco;
            font-size: 16px;
            color: {COLORS['fg']};
            '''
        credit_button.setStyleSheet(button_format)
        debit_button.setStyleSheet(button_format)

        account_type_layout.addWidget(label_description)
        account_type_layout.addWidget(credit_button)
        account_type_layout.addWidget(debit_button)

        self.layout.addLayout(account_type_layout)

        # continue button
        self.layout.addSpacing(25)

        continue_button_layout = QHBoxLayout()
        self.continue_button = QPushButton('Continue')
        self.continue_button.setFixedSize(150, 50)
        self.continue_button.clicked.connect(self.continue_button_pressed)
        self.continue_button.setDisabled(True)
        continue_shortcut = QShortcut(QKeySequence('Return'), self)
        continue_shortcut.activated.connect(self.continue_button.click)

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
        continue_button_layout.addWidget(self.continue_button)
        continue_button_layout.addStretch()
        self.layout.addLayout(continue_button_layout)
        #self.layout.addWidget(self.continue_button)


        # footer
        keys_functions = [('h', 'go home'),
                          ('o', 'open file'),
                          ('c', 'credit'),
                          ('d', 'debit'),
                          ('<return>', 'continue'),
                         ]
        self.layout.addStretch()
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

    def open_file_dialog(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV Files (*.csv)')
        if self.filename:
            if Path(self.filename).exists():
                self.import_label.setText(f'{self.filename}')
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

        self.check_activate_continue_button()
        
    def check_activate_continue_button(self):
        if self.account and self.file_exists:
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
        print('continue')

    def go_home(self):
        self.stacked_widget.setCurrentIndex(SCREENS.HOME)
