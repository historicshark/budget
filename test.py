from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy
)

class ButtonRowWithFooter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rows with Footer")
        self.setMinimumSize(400, 300)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # === Rows ===
        row_layout = QVBoxLayout()
        row_layout.setSpacing(10)  # Fixed spacing between rows

        for i in range(5):
            h = QHBoxLayout()
            btn = QPushButton(f"Button {i+1}")
            label = QLabel(f"This is description for Button {i+1}")
            h.addWidget(btn)
            h.addWidget(label)
            h.addStretch()  # push label to left and keep consistent spacing
            row_layout.addLayout(h)

        main_layout.addLayout(row_layout)

        # === Spacer to push footer down ===
        main_layout.addStretch()

        # === Footer ===
        footer = QLabel("This is the footer")
        footer.setStyleSheet("color: gray; border-top: 1px solid #ccc; padding-top: 5px;")
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication([])
    window = ButtonRowWithFooter()
    window.show()
    app.exec_()

