from PyQt5.QtWidgets import (
    QWidget,
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QShortcut,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

class CollapsibleGroupBox(QGroupBox):
    """
    Contains a header that can be clicked to expand/collapse the group. Content
    is stored in a QVBoxLayout. A shortcut can be added to expand/collapse the
    widget.
    
    Use addWidget or addLayout to add to the group.
    """
    def __init__(self, title: str, shortcut_key=None, parent=None):
        super().__init__()
        self.setTitle("")
        self.setCheckable(False)
        self.shortcut_key = shortcut_key

        # Create header with toggle button
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(5, 5, 5, 5)

        self.header_text = f'▼ {title}'
        self.toggle_button = QPushButton(self.header_text)
        self.toggle_button.setFlat(True)
        self.toggle_button.clicked.connect(self.toggle_content)

        if self.shortcut_key and parent:
            self.shortcut = QShortcut(QKeySequence(self.shortcut_key), parent)
            self.shortcut.activated.connect(self.toggle_content)

        header_layout.addWidget(self.toggle_button)
        header_layout.addStretch()

        # Create content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(header_widget)
        main_layout.addWidget(self.content_widget)

        self.expanded = True
        self.toggle_content()

    def toggle_content(self):
        font = self.toggle_button.font()
        if self.expanded:
            self.content_widget.hide()
            self.toggle_button.setText(self.header_text.replace("▼", "▶"))
            self.expanded = False
            font.setBold(False)
        else:
            self.content_widget.show()
            self.toggle_button.setText(self.header_text.replace("▶", "▼"))
            self.expanded = True
            font.setBold(True)
        self.toggle_button.setFont(font)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)

    def addLayout(self, layout):
        self.content_layout.addLayout(layout)

