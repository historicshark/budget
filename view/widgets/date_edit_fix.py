from PyQt5.QtWidgets import QDateEdit, QStyleOptionSpinBox, QTableView
from PyQt5.QtCore import Qt, QTimer, QEvent, QDate
from PyQt5.QtGui import QMouseEvent, QColor
import datetime
from view.default_style_sheet import colors

class DateEditFix(QDateEdit):
    """
    QDateEdit with a timer to reset style after date from popup calendar is chosen
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setMouseTracking(True)
        self._hover_button = False

        self.dateChanged.connect(self.start_timer)

        self.hover_reset_timer = QTimer()
        self.hover_reset_timer.timeout.connect(self.reset_hover_state)
        self.hover_reset_timer.setSingleShot(True)

        calendar = self.calendarWidget()
        fmt = calendar.headerTextFormat()
        fmt.setForeground(QColor(colors['fg0']))
        fmt.setBackground(QColor(colors['bg2']))
        calendar.setHeaderTextFormat(fmt)

    def start_timer(self, index):
        self.hover_reset_timer.start(100)

    def reset_hover_state(self):
        self.setAttribute(Qt.WA_UnderMouse, False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mouseMoveEvent(self, event):
        # Get the drop-down button rectangle
        opt = QStyleOptionSpinBox()
        self.initStyleOption(opt)
        button_rect = self.style().subControlRect(
            self.style().CC_ComboBox, opt,
            self.style().SC_ComboBoxArrow, self
        )

        # Check if mouse is over the button
        was_hovering = self._hover_button
        self._hover_button = button_rect.contains(event.pos())

        # Update style if hover state changed
        if was_hovering != self._hover_button:
            self.update()

        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self._hover_button:
            self._hover_button = False
            self.update()
        super().leaveEvent(event)

#    this resets style when calendar popup opens
#    def focusOutEvent(self, event):
#        super().focusOutEvent(event)
#        self.start_timer()
    
    def set_date_today(self):
        self.setDate(QDate().fromString(str(datetime.date.today()), Qt.ISODate))
