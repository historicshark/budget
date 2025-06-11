from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import Qt, QTimer

class DateEditFix(QDateEdit):
    """
    QDateEdit with a timer to reset style after date from popup calendar is chosen
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)

        self.dateChanged.connect(self.start_timer)

        self.hover_reset_timer = QTimer()
        self.hover_reset_timer.timeout.connect(self.reset_hover_state)
        self.hover_reset_timer.setSingleShot(True)

    def start_timer(self):
        self.hover_reset_timer.start(100)

    def reset_hover_state(self):
        self.setAttribute(Qt.WA_UnderMouse, False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

#    this resets style when calendar popup opens
#    def focusOutEvent(self, event):
#        super().focusOutEvent(event)
#        self.start_timer()

