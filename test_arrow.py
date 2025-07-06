import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateEdit, QLabel
from PyQt5.QtCore import QDate

class SizedArrowExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Default for comparison
        layout.addWidget(QLabel("Default (no styling):"))
        default_date_edit = QDateEdit(self)
        default_date_edit.setDate(QDate.currentDate())
        layout.addWidget(default_date_edit)
        
        # Wide button with small arrow
        layout.addWidget(QLabel("Wide button, small arrow:"))
        date_edit1 = QDateEdit(self)
        date_edit1.setDate(QDate.currentDate())
        date_edit1.setCalendarPopup(True)
        date_edit1.setStyleSheet("""
            QDateEdit {
                background-color: #ffffff;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 40px;  /* Wide button */
                border-left: 1px solid #3498db;
                background-color: #f8f9fa;
            }
            QDateEdit::down-arrow {
                width: 12px;   /* Small arrow width */
                height: 8px;   /* Small arrow height */
            }
        """)
        layout.addWidget(date_edit1)
        
        # Very wide button with tiny arrow
        layout.addWidget(QLabel("Very wide button, tiny arrow:"))
        date_edit2 = QDateEdit(self)
        date_edit2.setDate(QDate.currentDate())
        date_edit2.setCalendarPopup(True)
        date_edit2.setStyleSheet("""
            QDateEdit {
                background-color: #ffffff;
                border: 2px solid #e74c3c;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 60px;  /* Very wide button */
                border-left: 1px solid #e74c3c;
                background-color: #f8f9fa;
            }
            QDateEdit::down-arrow {
                width: 8px;    /* Tiny arrow width */
                height: 6px;   /* Tiny arrow height */
            }
        """)
        layout.addWidget(date_edit2)
        
        # You can also position the arrow within the button area
        layout.addWidget(QLabel("Wide button, positioned small arrow:"))
        date_edit3 = QDateEdit(self)
        date_edit3.setDate(QDate.currentDate())
        date_edit3.setCalendarPopup(True)
        date_edit3.setStyleSheet("""
            QDateEdit {
                background-color: #ffffff;
                border: 2px solid #9b59b6;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 50px;
                border-left: 1px solid #9b59b6;
                background-color: #f8f9fa;
            }
            QDateEdit::down-arrow {
                subcontrol-origin: padding;
                subcontrol-position: center;  /* Center the arrow in the button */
                width: 10px;
                height: 7px;
            }
        """)
        layout.addWidget(date_edit3)
        
        self.setLayout(layout)
        self.setWindowTitle('Sized Arrow Examples')
        self.setGeometry(300, 300, 400, 400)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SizedArrowExample()
    sys.exit(app.exec_())
