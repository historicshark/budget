from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QFileDialog,
)

from PyQt5.QtCore import Qt

from global_variables import COLORS, SCREENS


class ImportScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.filename = ''
        self.initUI()

    def initUI(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10,10,10,10)
        
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
                            font-size: 18px;
                            color: {COLORS['orange']};
                            ''')

        row_layout.addWidget(import_button)
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
            font-size: 18px;
            color: {COLORS['fg']};
            '''
        credit_button.setStyleSheet(button_format)
        debit_button.setStyleSheet(button_format)

        account_type_layout.addWidget(label_description)
        account_type_layout.addWidget(credit_button)
        account_type_layout.addWidget(debit_button)

        self.layout.addLayout(account_type_layout)

        # footer
        keys_functions = [('h', 'go home'),
                          ('o', 'open file'),
                          ('c', 'credit'),
                          ('d', 'debit'),
                         ]
        self.layout.addStretch()
        footer = QLabel(' • '.join([f'({key}): {function}' for key, function in keys_functions]))
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
            print('credit')

    def debit_button_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            print('debit')

    def open_file_dialog(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV Files (*.csv)')
        if self.filename:
            self.import_label.setText(f'{self.filename}')
            self.import_label.setStyleSheet(f'''
                            font-family: Monaco;
                            font-size: 18px;
                            color: {COLORS['fg']};
                            ''')
            print(self.filename)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(SCREENS.HOME)
