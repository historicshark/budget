from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QPushButton,
    QShortcut,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from string import ascii_lowercase

from global_variables import COLORS, SCREENS
from fcn.import_categorize import Importer


class CategorizeScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget, importer: Importer):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout()
        self.importer = importer
        self.category = ''

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

        # Two columns showing transaction and category options
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # Left column - current transaction being categorized and the continue and cancel buttons
        left_layout.addSpacing(10)

        self.location_label = QLabel('Transaction: ')
        self.date_label = QLabel('Date: ')
        self.amount_label = QLabel('Amount: $')

        left_layout.addWidget(self.location_label)
        left_layout.addWidget(self.date_label)
        left_layout.addWidget(self.amount_label)

        label_style = f'''
                      font-family: Monaco;
                      font-size: 20px;
                      color: {COLORS['fg']};
                      margin: 3px;
                      '''
        self.location_label.setStyleSheet(label_style)
        self.date_label.setStyleSheet(label_style)
        self.amount_label.setStyleSheet(label_style)

        left_layout.addStretch()
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
                               background-color: {COLORS['gray']};
                               color: {COLORS['bg']};
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
        left_layout.addLayout(continue_button_layout)

        # right layout
        category_label = QLabel('Choose a category:')
        category_label.setStyleSheet(label_style)
        self.update_category_buttons()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(self.right_layout)

        self.layout.addLayout(main_layout)
        self.setLayout(self.layout)

        # footer
        keys_functions = [('<return>', 'continue'),
                          ('<esc>', 'cancel'),
                          ('<key>', 'select category'),
                         ]
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

    def display_transaction(self, record: dict[str, str]):
        self.location_label.setText(f'Transaction: {record["Location"]}')
        self.date_label.setText(f'Date: {record["Date"]}')
        self.amount_label.setText(f'Amount: ${record["Amount"]}')

    def update_category_buttons(self):
        style = f'''
                font-family: Monaco;
                font-size: 16px;
                color: {COLORS['fg']};
                '''
        spacing = 25
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        for key, category in zip(ascii_lowercase, self.importer.categories):
            row = QHBoxLayout()
            key_label = QLabel(f'({key})')
            button = QRadioButton(category.replace('&', '&&'))
            button.setShortcut(key)
            button.toggled.connect(self.category_button_toggled)

            key_label.setStyleSheet(style)
            button.setStyleSheet(style)
            row.addWidget(key_label)
            row.addWidget(button)
            row.addSpacing(spacing)
            row.addStretch()
            layout.addLayout(row)
        
        row = QHBoxLayout()
        key_label = QLabel('   ')
        button = QRadioButton('New Category')
        button.toggled.connect(self.category_button_toggled)
        key_label.setStyleSheet(style)
        button.setStyleSheet(style)
        row.addWidget(key_label)
        row.addWidget(button)
        row.addSpacing(spacing)
        row.addStretch()
        layout.addLayout(row)

        layout.addStretch()
        self.right_layout.addWidget(container, alignment=Qt.AlignRight)

    def category_button_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            tmp = sender.text().replace('&&','&')
            print(tmp)
            self.category = tmp

    def continue_button_pressed(self):
        print('continue')
    
    def cancel_button_pressed(self):
        self.stacked_widget.setCurrentIndex(SCREENS.IMPORT)

    def go_home(self):
        self.stacked_widget.setCurrentIndex(SCREENS.HOME)