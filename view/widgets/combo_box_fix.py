from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QMouseEvent

class ComboBoxFix(QComboBox):
    """
    QComboBox with a timer to reset style 
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_menu_open = False
        self.activated.connect(self.start_timer)

        self.hover_reset_timer = QTimer()
        self.hover_reset_timer.timeout.connect(self.reset_hover_state)
        self.hover_reset_timer.setSingleShot(True)

    def showPopup(self):
        self.reset_hover_state()
        super().showPopup()

    def start_timer(self):
        self.hover_reset_timer.start(100)

    def reset_hover_state(self):
        self.setAttribute(Qt.WA_UnderMouse, False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

