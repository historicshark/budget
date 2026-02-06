from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import QSize
from view import colors

class ProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(30)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.color = colors['green']
        self.maximum = 100
        self.value = 25
        self.radius = 5

    def paintEvent(self, event):
        if self.maximum <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        pen = QPen(QColor(colors['fg']), 2)
        painter.setPen(pen)

        if self.value <= self.maximum:
            painter.drawRoundedRect(1, 1, w-2, h-2, self.radius, self.radius)

            fill_ratio = self.value / self.maximum
            fill_width = int(fill_ratio*(w-4))

            clip_path = QPainterPath()
            r = self.radius - 1 if self.radius > 1 else 0
            clip_path.addRoundedRect(2, 2, fill_width, h-4, r, r)
            painter.setClipPath(clip_path)

            painter.fillRect(2, 2, fill_width, h-4, QColor(self.color))

        else:
            border_ratio = self.maximum / self.value

            clip_path = QPainterPath()
            r = self.radius - 1 if self.radius > 1 else 0
            clip_path.addRoundedRect(2, 2, w-4, h-4, r, r)
            painter.setClipPath(clip_path)
            painter.fillRect(2, 2, w-4, h-4, QColor(self.color))

            painter.setClipping(False)
            painter.drawRoundedRect(1, 1, int(border_ratio*(w-2)), h-2, self.radius, self.radius)

    def sizeHint(self):
        return QSize(500, 20)

    def plot(self, maximum: float, value: float, color=None):
        if color is None:
            self.color = colors['green'] if value < maximum else colors['red']
        self.maximum = maximum
        self.value = value
        self.update()
