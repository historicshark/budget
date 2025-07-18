from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QPushButton,
    QShortcut,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from view import colors

class BaseScreen(QWidget):
    """
    screen with
    - base_layout (QVBoxLayout) with no margins
    - content_layout (QVBoxLayout) with 15px margins left and right
    """
    def __init__(self):
        super().__init__()

        self.base_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.base_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setContentsMargins(15,0,15,0)
        self.base_layout.addLayout(self.content_layout)

        self.setLayout(self.base_layout)

    def add_title(self, owner_layout, title: str, home_clicked_emit, spacing=50):
        title_layout = QHBoxLayout()

        label_title = QLabel(title)
        label_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label_title.setObjectName('title')
        label_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        home_button = QPushButton('Home')
        home_button.clicked.connect(home_clicked_emit)
        home_button.setObjectName('home')
        home_button.setFixedSize(70, 30)

        title_layout.addWidget(home_button)
        title_layout.addWidget(label_title)
        title_layout.addSpacing(70)

        owner_layout.addLayout(title_layout)
        owner_layout.addSpacing(spacing)

    def add_continue_cancel_buttons(self, owner_layout, continue_clicked_connect, cancel_clicked_connect, add_stretch=True) -> QHBoxLayout:
        """
        adds shortcuts 'Return' and 'Escape' to Continue and Cancel buttons
        add_stretch: add stretch to the end of the QHBoxLayout containing the buttons
        returns the layout containing the buttons
        """
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
        self.cancel_button.setStyleSheet(f'QPushButton:hover {{ background-color: {colors["orange-faded"]}; }}')

        layout.addWidget(self.continue_button)
        layout.addSpacing(20)
        layout.addWidget(self.cancel_button)
        if add_stretch:
            layout.addStretch()
        owner_layout.addLayout(layout)
        return layout

    def add_footer(self, owner_layout, keys_functions: list[tuple[str, str]]):
        self.footer = QLabel(' • '.join([f'{function}: {key}' for key, function in keys_functions]))
        self.footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.footer.setObjectName('footer')
        owner_layout.addWidget(self.footer)

    def update_footer(self, keys_functions: list[tuple[str, str]]):
        self.footer.setText(' • '.join([f'{function}: {key}' for key, function in keys_functions]))

    def clear_layout(self, layout: QLayout):
        """
        https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        """
        print(f'--- clearing layout {layout}')
        for i in reversed(range(layout.count())):
            layout_item = layout.itemAt(i)
            if layout_item.widget() is not None:
                widget_to_remove = layout_item.widget()
                print(f'removing widget {widget_to_remove}')
                widget_to_remove.setParent(None)
                layout.removeWidget(widget_to_remove)
            elif layout_item.spacerItem() is not None:
                print(f'removing spacer {layout_item.spacerItem()}')
            else:
                layout_to_remove = layout.itemAt(i)
                print(f'-- found Layout: {layout_to_remove}')
                self.clear_layout(layout_to_remove)
        print('--- clear complete')

    def reset(self):
        print(f'In {self.__class__.__name__}, reset not implemented!') #XXX debug

    def add_debug_borders(self, colors=None):
        """Add colored borders to widget and all child widgets"""
        if colors is None:
            colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']

        def apply_borders(w, depth=0):
            color = colors[depth % len(colors)]
            current_style = w.styleSheet()
            new_style = f"{current_style}; border: 2px solid {color};"
            w.setStyleSheet(new_style)

            # Recursively apply to children
            for child in w.findChildren(QWidget):
                if child.parent() == w:  # Only direct children
                    apply_borders(child, depth + 1)

        apply_borders(self)

