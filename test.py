from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt

app = QApplication([])

main_widget = QWidget()
main_layout = QVBoxLayout()
main_layout.setContentsMargins(20, 20, 20, 20)  # Layout has margins

# Add some content before the label
label1 = QLabel('above label')
label1.setStyleSheet("padding: 0px; margin: 0px; border: none; background-color: #b8bb26;")
main_layout.addWidget(label1)

# Create a special HBoxLayout with no margins or spacing
row_layout = QHBoxLayout()
row_layout.setContentsMargins(0, 0, 0, 0)
row_layout.setSpacing(0)

label = QLabel("This label ignores layout margins")
label.setStyleSheet("padding: 0px; margin: 0px; border: none; background-color: #b8bb26;")
label.setAlignment(Qt.AlignLeft)

row_layout.addWidget(label)

# Add the row layout via a wrapper widget
row_widget = QWidget()
row_widget.setLayout(row_layout)

main_layout.addWidget(row_widget)

main_widget.setLayout(main_layout)
main_widget.show()
app.exec_()

