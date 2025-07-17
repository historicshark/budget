import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTextEdit, QListWidget, QShortcut)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont

class TabWidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTabWidget Example with Shortcuts and Styling")
        self.setGeometry(100, 100, 800, 600)
        
        # Create the main tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Set up tabs
        self.create_tabs()
        
        # Set up keyboard shortcuts
        self.setup_shortcuts()
        
        # Apply styling
        self.apply_styling()
        
    def create_tabs(self):
        # Tab 1: Text Editor
        tab1 = QWidget()
        layout1 = QVBoxLayout()
        
        label1 = QLabel("Text Editor Tab")
        label1.setFont(QFont("Arial", 12, QFont.Bold))
        text_edit = QTextEdit()
        text_edit.setPlainText("This is a text editor in the first tab.")
        
        layout1.addWidget(label1)
        layout1.addWidget(text_edit)
        layout1.addStretch()
        tab1.setLayout(layout1)
        
        # Add tab with icon and tooltip
        self.tab_widget.addTab(tab1, "Editor")
        self.tab_widget.setTabToolTip(0, "Text editor for writing content")
        
        # Tab 2: List View
        tab2 = QWidget()
        layout2 = QVBoxLayout()
        
        label2 = QLabel("List View Tab")
        label2.setFont(QFont("Arial", 12, QFont.Bold))
        list_widget = QListWidget()
        for i in range(1, 11):
            list_widget.addItem(f"Item {i}")
        
        layout2.addWidget(label2)
        layout2.addWidget(list_widget)
        tab2.setLayout(layout2)
        
        self.tab_widget.addTab(tab2, "List")
        self.tab_widget.setTabToolTip(1, "List of items")
        
        # Tab 3: Controls
        tab3 = QWidget()
        layout3 = QVBoxLayout()
        
        label3 = QLabel("Controls Tab")
        label3.setFont(QFont("Arial", 12, QFont.Bold))
        
        button_layout = QHBoxLayout()
        btn1 = QPushButton("Button 1")
        btn2 = QPushButton("Button 2")
        btn3 = QPushButton("Close Tab")
        btn3.clicked.connect(self.close_current_tab)
        
        button_layout.addWidget(btn1)
        button_layout.addWidget(btn2)
        button_layout.addWidget(btn3)
        
        layout3.addWidget(label3)
        layout3.addLayout(button_layout)
        layout3.addStretch()
        tab3.setLayout(layout3)
        
        self.tab_widget.addTab(tab3, "Controls")
        self.tab_widget.setTabToolTip(2, "Various controls and buttons")
        
        # Tab 4: Closable tab
        tab4 = QWidget()
        layout4 = QVBoxLayout()
        layout4.addWidget(QLabel("This tab can be closed"))
        tab4.setLayout(layout4)
        
        self.tab_widget.addTab(tab4, "Closable")
        
        # Enable tab closing
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
    def setup_shortcuts(self):
        # Keyboard shortcuts for tab navigation
        
        # Ctrl+1, Ctrl+2, etc. to switch to specific tabs
        for i in range(1, 10):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i}"), self)
            shortcut.activated.connect(lambda checked, tab_index=i-1: self.switch_to_tab(tab_index))
        
        # Ctrl+Tab to go to next tab
        next_tab_shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
        next_tab_shortcut.activated.connect(self.next_tab)
        
        # Ctrl+Shift+Tab to go to previous tab
        prev_tab_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
        prev_tab_shortcut.activated.connect(self.previous_tab)
        
        # Ctrl+W to close current tab
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)
        
        # Ctrl+T to add new tab
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)
        
        # Alt+Left/Right for tab navigation
        alt_left = QShortcut(QKeySequence("Alt+Left"), self)
        alt_left.activated.connect(self.previous_tab)
        
        alt_right = QShortcut(QKeySequence("Alt+Right"), self)
        alt_right.activated.connect(self.next_tab)
        
    def apply_styling(self):
        # Custom stylesheet for the tab widget
        style = """
        QTabWidget::pane {
            border: 2px solid #C0C0C0;
            background-color: #F0F0F0;
            border-radius: 5px;
        }
        
        QTabBar::tab {
            background-color: #E0E0E0;
            border: 1px solid #C0C0C0;
            border-bottom: none;
            padding: 8px 16px;
            margin: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            min-width: 80px;
        }
        
        QTabBar::tab:selected {
            background-color: #4A90E2;
            color: white;
            font-weight: bold;
        }
        
        QTabBar::tab:hover {
            background-color: #B0B0B0;
        }
        
        QTabBar::tab:!selected {
            margin-top: 4px;
        }
        
        QTabBar::close-button {
            image: url(close.png);
            subcontrol-position: right;
        }
        
        QTabBar::close-button:hover {
            background-color: #FF6B6B;
            border-radius: 3px;
        }
        
        QTabWidget::tab-bar {
            left: 5px;
        }
        """
        
        self.tab_widget.setStyleSheet(style)
        
        # Set tab position (can be North, South, East, West)
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # Set tab shape (Rounded or Triangular)
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        
    def switch_to_tab(self, index):
        """Switch to a specific tab by index"""
        if 0 <= index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(index)
            
    def next_tab(self):
        """Switch to the next tab"""
        current = self.tab_widget.currentIndex()
        next_index = (current + 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(next_index)
        
    def previous_tab(self):
        """Switch to the previous tab"""
        current = self.tab_widget.currentIndex()
        prev_index = (current - 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(prev_index)
        
    def close_current_tab(self):
        """Close the currently active tab"""
        current_index = self.tab_widget.currentIndex()
        if self.tab_widget.count() > 1:  # Don't close if it's the last tab
            self.close_tab(current_index)
            
    def close_tab(self, index):
        """Close a tab by index"""
        if self.tab_widget.count() > 1:  # Keep at least one tab
            self.tab_widget.removeTab(index)
            
    def add_new_tab(self):
        """Add a new tab dynamically"""
        new_tab = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel(f"New Tab {self.tab_widget.count() + 1}")
        label.setFont(QFont("Arial", 12, QFont.Bold))
        text_edit = QTextEdit()
        text_edit.setPlainText("This is a dynamically created tab.")
        
        layout.addWidget(label)
        layout.addWidget(text_edit)
        new_tab.setLayout(layout)
        
        # Add the new tab and switch to it
        index = self.tab_widget.addTab(new_tab, f"New {self.tab_widget.count()}")
        self.tab_widget.setCurrentIndex(index)

def main():
    app = QApplication(sys.argv)
    
    window = TabWidgetExample()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
