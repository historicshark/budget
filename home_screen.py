from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)

from PyQt5.QtCore import Qt

from global_variables import COLORS


class HomeScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
    
        self.button_labels_descriptions_methods_keys = [
            ('import', 'Import a csv file on your computer', self.on_click_import, 'i'),
            ('plot', 'Display a plot', self.on_click_plot, 'p'),
            ('list', 'List transactions', self.on_click_list, 'l'),
        ]
        
        self.layout = QVBoxLayout()
        self.row_layout = QVBoxLayout()

        self.initUI()

    def initUI(self):
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10,10,10,10)

        self.row_layout.setSpacing(10)

        # Screen title
        label_title = QLabel('Home')
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label_title.setStyleSheet(f'''
                                  font-family: Monaco;
                                  font-size: 25px;
                                  color: {COLORS['fg']};
                                  margin: 10px;
                                  ''')
        self.layout.addWidget(label_title)

        # Button rows
        for button_label, button_description, method, key in self.button_labels_descriptions_methods_keys:
            row = QHBoxLayout()

            button = QPushButton(button_label)
            button.setFixedSize(150, 50)
            button.clicked.connect(method)
            button.setShortcut(key)

            label = QLabel(button_description)

            button.setStyleSheet(f'''
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

            label.setStyleSheet(f'''
                                font-family: Monaco;
                                font-size: 18px;
                                color: {COLORS['fg']};
                                ''')

            row.addWidget(button)
            row.addWidget(label)
            row.addStretch()

            self.row_layout.addLayout(row)

        self.layout.addLayout(self.row_layout)

        # footer
        self.layout.addStretch()
        footer = QLabel(' • '.join([f'({key}): {button}' for button, _, _, key in self.button_labels_descriptions_methods_keys]))
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


    def on_click_import(self):
        print('import')

    def on_click_plot(self):
        print('plot')

    def on_click_list(self):
        print('list')

