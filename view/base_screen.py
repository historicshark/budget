from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QPushButton,
    QShortcut,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from view.default_style_sheet import colors

class BaseScreen(QWidget):
    def __init__(self):
        super().__init__()
    
    def add_title(self, owner_layout, title: str, home_clicked_connect):
        title_layout = QHBoxLayout()

        label_title = QLabel(title)
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label_title.setObjectName('title')

        home_button = QPushButton('Home')
        home_button.clicked.connect(home_clicked_connect)
        home_button.setObjectName('home')
        home_button.setFixedSize(70, 30)

        title_layout.addWidget(home_button)
        title_layout.addWidget(label_title)
        title_layout.addSpacing(70)

        owner_layout.addLayout(title_layout)
        owner_layout.addSpacing(50)
    
    def add_continue_cancel_buttons(self, owner_layout, continue_clicked_connect, cancel_clicked_connect):
        layout = QHBoxLayout()

        self.continue_button = QPushButton('Continue')
        self.continue_button.setFixedSize(150, 50)
        self.continue_button.clicked.connect(continue_clicked_connect)
        continue_shortcut = QShortcut(QKeySequence('Return'), self)
        continue_shortcut.activated.connect(self.continue_button.click)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setFixedSize(150, 50)
        self.cancel_button.clicked.connect(cancel_clicked_connect)
        cancel_shortcut = QShortcut(QKeySequence('Escape'), self)
        cancel_shortcut.activated.connect(self.cancel_button.click)
        self.cancel_button.setStyleSheet(f'QPushButton:hover {{ background-color: {colors['orange']}; }}')

        layout.addWidget(self.continue_button)
        layout.addSpacing(20)
        layout.addWidget(self.cancel_button)
        layout.addStretch()
        owner_layout.addLayout(layout)
    
    def add_footer(self, owner_layout, keys_functions: list[tuple[str, str]]):
        footer = QLabel(' • '.join([f'{function}: {key}' for key, function in keys_functions]))
        footer.setObjectName('footer')
        owner_layout.addWidget(footer)

