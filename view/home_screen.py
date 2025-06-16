from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)
from PyQt5.QtCore import Qt, pyqtSignal

from view.base_screen import BaseScreen

class HomeScreen(BaseScreen):
    import_clicked = pyqtSignal()
    plot_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()    
        self.button_labels_descriptions_methods_keys = [
            ('import', 'Import a file on your computer', self.import_clicked.emit, 'i'),
            ('plot', 'Display a plot', self.plot_clicked.emit, 'p'),
            # ('list', 'List transactions', self.on_click_list, 'l'),
        ]

        self.initUI()

    def initUI(self):
        self.base_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.base_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setContentsMargins(15,0,15,0)
        self.base_layout.addLayout(self.content_layout)

        # Screen title
        label_title = QLabel('Home')
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label_title.setObjectName('title')
        self.content_layout.addWidget(label_title)

        # Button rows
        button_layout = QFormLayout()
        button_layout.setVerticalSpacing(20)
        button_layout.setFormAlignment(Qt.AlignLeft)
        button_layout.setHorizontalSpacing(20)
        for button_label, button_description, method, key in self.button_labels_descriptions_methods_keys:
            button = QPushButton(button_label)
            button.setFixedSize(150, 50)
            button.clicked.connect(method)
            button.setShortcut(key)

            label = QLabel(button_description)

            button_layout.addRow(button, label)

        self.content_layout.addLayout(button_layout)

        self.content_layout.addStretch()
        self.add_footer(self.base_layout, [(key, function) for function, _, _, key in self.button_labels_descriptions_methods_keys])

        self.setLayout(self.base_layout)

