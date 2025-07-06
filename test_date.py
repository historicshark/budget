import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateEdit, QLabel
from PyQt5.QtCore import QDate

class StyledDateEditExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Create multiple styled date edits
        self.create_modern_date_edit(layout)
        self.create_dark_date_edit(layout)
        self.create_colorful_date_edit(layout)
        
        self.setLayout(layout)
        self.setWindowTitle('Styled QDateEdit Examples')
        self.setGeometry(300, 300, 400, 300)
        self.show()
    
    def create_modern_date_edit(self, layout):
        layout.addWidget(QLabel("Modern Style:"))
        
        modern_date_edit = QDateEdit(self)
        modern_date_edit.setDate(QDate.currentDate())
        modern_date_edit.setCalendarPopup(True)
        
        modern_date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #ffffff;
                border: 2px solid #e1e1e1;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #333333;
            }
            
            QDateEdit:hover {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
            
            QDateEdit:focus {
                border-color: #2980b9;
                background-color: #ffffff;
                outline: none;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #e1e1e1;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                background-color: #f8f9fa;
            }
            
            QDateEdit::drop-down:hover {
                background-color: #e9ecef;
            }
            
            QDateEdit::down-arrow {
                image: none;
                border: 2px solid #666666;
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                margin-top: -2px;
            }
                                       QCalendarWidget {
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }

    QCalendarWidget QToolButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 5px;
    }

    QCalendarWidget QAbstractItemView {
        background-color: #ffffff;
        selection-background-color: #3498db;
        selection-color: white;
    }

    QCalendarWidget QAbstractItemView:enabled {
        color: #333333;
    }
        """)
        
        layout.addWidget(modern_date_edit)
    
    def create_dark_date_edit(self, layout):
        layout.addWidget(QLabel("Dark Theme:"))
        
        dark_date_edit = QDateEdit(self)
        dark_date_edit.setDate(QDate.currentDate())
        dark_date_edit.setCalendarPopup(True)
        
        dark_date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
                color: #ecf0f1;
            }
            
            QDateEdit:hover {
                border-color: #3498db;
                background-color: #34495e;
            }
            
            QDateEdit:focus {
                border-color: #e74c3c;
                background-color: #2c3e50;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #34495e;
                background-color: #34495e;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            
            QDateEdit::drop-down:hover {
                background-color: #3498db;
            }
            
            QDateEdit::down-arrow {
                image: none;
                border: 2px solid #ecf0f1;
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
            }
        """)
        
        layout.addWidget(dark_date_edit)
    
    def create_colorful_date_edit(self, layout):
        layout.addWidget(QLabel("Colorful Style:"))
        
        colorful_date_edit = QDateEdit(self)
        colorful_date_edit.setDate(QDate.currentDate())
        colorful_date_edit.setCalendarPopup(True)
        
        colorful_date_edit.setStyleSheet("""
            QDateEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9a9e, stop:1 #fecfef);
                border: 3px solid #ff6b9d;
                border-radius: 15px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            
            QDateEdit:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffeaa7, stop:1 #fab1a0);
                border-color: #e17055;
            }
            
            QDateEdit:focus {
                border-color: #0984e3;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #74b9ff, stop:1 #0984e3);
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 2px solid #ff6b9d;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, stop:1 rgba(255,255,255,0.2));
            }
            
            QDateEdit::down-arrow {
                image: none;
                border: 3px solid #ffffff;
                width: 8px;
                height: 8px;
                border-top: none;
                border-left: none;
            }
        """)
        
        layout.addWidget(colorful_date_edit)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StyledDateEditExample()
    sys.exit(app.exec_())
