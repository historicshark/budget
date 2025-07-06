import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox

app = QApplication(sys.argv)
window = QWidget()

checkbox = QCheckBox("Custom styled checkbox")
checkbox.setStyleSheet("""
    QCheckBox {
        font-size: 16px;
        color: #2c3e50;
        font-weight: bold;
        spacing: 8px;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
    }
    
    QCheckBox::indicator:unchecked {
        border: 2px solid #bdc3c7;
        background-color: #ecf0f1;
        border-radius: 4px;
    }
    
    QCheckBox::indicator:checked {
        border: 2px solid #27ae60;
        background-color: #27ae60;
        border-radius: 4px;
    }
    
    QCheckBox::indicator:checked::after {
        content: "✓";
        color: white;
        font-weight: bold;
    }
""")

layout = QVBoxLayout()
layout.addWidget(checkbox)
window.setLayout(layout)
window.show()

sys.exit(app.exec_())
