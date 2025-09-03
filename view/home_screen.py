from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)
from PyQt5.QtCore import Qt, pyqtSignal

from view import BaseScreen

class HomeScreen(BaseScreen):
    import_clicked = pyqtSignal()
    expenses_clicked = pyqtSignal()
    list_clicked = pyqtSignal()
    create_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()    
        self.button_labels_descriptions_methods_keys = [
            ('import', 'Import a file on your computer', self.import_clicked.emit, 'i'),
            ('expenses', 'Visualize expenses', self.expenses_clicked.emit, 'e'),
            ('list', 'List, edit, and delete transactions', self.list_clicked.emit, 'l'),
            ('create', 'Manually create a transaction', self.create_clicked.emit, 'c'),
        ]

        self.initUI()

    def initUI(self):
        # Screen title
        label_title = QLabel('Home')
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label_title.setObjectName('title')
        self.content_layout.addWidget(label_title)
        self.content_layout.addSpacing(30)

        # Button rows
        button_layout = QFormLayout()
        button_layout.setVerticalSpacing(30)
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

