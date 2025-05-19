from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, pyqtSignal

from view.base_screen import BaseScreen

class HomeScreen(BaseScreen):
    import_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()    
        self.button_labels_descriptions_methods_keys = [
            ('import', 'Import a csv file on your computer', self.import_clicked.emit, 'i'),
            # ('plot', 'Display a plot', self.on_click_plot, 'p'),
            # ('list', 'List transactions', self.on_click_list, 'l'),
        ]
        
        self.layout = QVBoxLayout()

        self.initUI()

    def initUI(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15,0,15,0)

        row_layout = QVBoxLayout()
        row_layout.setSpacing(10)

        # Screen title
        label_title = QLabel('Home')
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label_title.setObjectName('title')
        self.layout.addWidget(label_title)

        # Button rows
        for button_label, button_description, method, key in self.button_labels_descriptions_methods_keys:
            row = QHBoxLayout()

            button = QPushButton(button_label)
            button.setFixedSize(150, 50)
            button.clicked.connect(method)
            button.setShortcut(key)

            label = QLabel(button_description)

            row.addWidget(button)
            row.addWidget(label)
            row.addStretch()

            row_layout.addLayout(row)

        self.layout.addLayout(row_layout)

        self.layout.addStretch()
        self.add_footer(self.layout, [(key, function for button, _, _, key in self.button_labels_descriptions_methods_keys)])

        self.setLayout(self.layout)
