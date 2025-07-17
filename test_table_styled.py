import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class StyledTableExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget Styling Examples")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create table widget
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(['Name', 'Age', 'City', 'Score'])
        
        # Add sample data
        sample_data = [
            ['John', '25', 'New York', '85'],
            ['Jane', '30', 'Los Angeles', '92'],
            ['Bob', '35', 'Chicago', '78'],
            ['Alice', '28', 'Houston', '88'],
            ['Charlie', '32', 'Phoenix', '90']
        ]
        
        for row, row_data in enumerate(sample_data):
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(value))
        
        # Apply comprehensive styling
        self.apply_comprehensive_styling()
        
        layout.addWidget(self.table)
    
    def apply_comprehensive_styling(self):
        """Apply comprehensive styling to the table"""
        stylesheet = """
        QTableWidget {
            background-color: #f5f5f5;
            alternate-background-color: #e8e8e8;
            selection-background-color: #3daee9;
            selection-color: white;
            gridline-color: #d0d0d0;
            border: 1px solid #c0c0c0;
        }
        
        QTableWidget::item {
            padding: 8px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background-color: #3daee9;
            color: white;
        }
        
        QTableWidget::item:hover {
            background-color: #bee6fd;
        }
        
        QHeaderView::section {
            background-color: #4a90e2;
            color: white;
            padding: 8px;
            border: 1px solid #357abd;
            font-weight: bold;
        }
        
        QHeaderView::section:hover {
            background-color: #357abd;
        }
        
        QHeaderView::section:pressed {
            background-color: #2868a3;
        }
        
        QTableWidget::corner {
            background-color: #4a90e2;
            border: 1px solid #357abd;
        }
        
        QScrollBar:vertical {
            background: #f0f0f0;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #a0a0a0;
        }
        """
        
        self.table.setStyleSheet(stylesheet)
        
        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)
    
    def apply_cell_specific_styling(self):
        """Example of styling specific cells programmatically"""
        # Style specific cells with background colors
        for row in range(self.table.rowCount()):
            score_item = self.table.item(row, 3)  # Score column
            if score_item:
                score = int(score_item.text())
                if score >= 90:
                    score_item.setBackground(QColor(144, 238, 144))  # Light green
                elif score >= 80:
                    score_item.setBackground(QColor(255, 255, 224))  # Light yellow
                else:
                    score_item.setBackground(QColor(255, 182, 193))  # Light pink

# Alternative styling approaches
class AlternativeStylingExamples:
    """Examples of different styling approaches"""
    
    @staticmethod
    def simple_alternating_colors(table):
        """Simple alternating row colors"""
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f0f0f0;
                background-color: white;
            }
        """)
    
    @staticmethod
    def custom_header_styling(table):
        """Custom header styling"""
        table.setStyleSheet("""
            QHeaderView::section {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #616161, stop: 0.5 #505050,
                                                stop: 0.6 #434343, stop:1 #656565);
                color: white;
                padding-left: 4px;
                border: 1px solid #6c6c6c;
                font-weight: bold;
            }
        """)
    
    @staticmethod
    def dark_theme_styling(table):
        """Dark theme styling"""
        table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                alternate-background-color: #3c3c3c;
                color: #ffffff;
                gridline-color: #555555;
                selection-background-color: #4a9eff;
                selection-color: white;
            }
            
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 4px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            
            QTableWidget::item {
                padding: 4px;
            }
            
            QTableWidget::item:selected {
                background-color: #4a9eff;
            }
        """)
    
    @staticmethod
    def programmatic_cell_styling(table):
        """Style cells programmatically without stylesheets"""
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    # Alternate row colors
                    if row % 2 == 0:
                        item.setBackground(QColor(240, 240, 240))
                    else:
                        item.setBackground(QColor(255, 255, 255))
                    
                    # Special styling for specific columns
                    if col == 0:  # First column
                        item.setBackground(QColor(230, 230, 250))  # Lavender

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StyledTableExample()
    window.show()
    sys.exit(app.exec_())
