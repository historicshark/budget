import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QCheckBox, QLabel, QGroupBox, 
                            QDateEdit, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QHeaderView, QFrame, QScrollArea,
                            QSplitter, QComboBox, QShortcut)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QKeySequence
from datetime import datetime, timedelta
import random

from view.widgets.collapsible_group_box import CollapsibleGroupBox
#class CollapsibleGroupBox(QGroupBox):
#    def __init__(self, title, shortcut_key=None, parent=None):
#        super().__init__(parent)
#        self.setTitle("")
#        self.setCheckable(False)
#        self.shortcut_key = shortcut_key
#        
#        # Create header with toggle button
#        header_widget = QWidget()
#        header_layout = QHBoxLayout(header_widget)
#        header_layout.setContentsMargins(5, 5, 5, 5)
#        
#        # Add shortcut info to button text if provided
#        button_text = f"▼ {title}"
#        if shortcut_key:
#            button_text += f" ({shortcut_key})"
#            
#        self.toggle_button = QPushButton(button_text)
#        self.toggle_button.setFlat(True)
#        self.toggle_button.clicked.connect(self.toggle_content)
#        font = self.toggle_button.font()
#        font.setBold(True)
#        self.toggle_button.setFont(font)
#        
#        header_layout.addWidget(self.toggle_button)
#        header_layout.addStretch()
#        
#        # Create content widget
#        self.content_widget = QWidget()
#        self.content_layout = QVBoxLayout(self.content_widget)
#        
#        # Main layout
#        main_layout = QVBoxLayout(self)
#        main_layout.setContentsMargins(0, 0, 0, 0)
#        main_layout.setSpacing(0)
#        main_layout.addWidget(header_widget)
#        main_layout.addWidget(self.content_widget)
#        
#        self.expanded = True
#        
#        # Setup keyboard shortcut if provided
#        self.shortcut = None
#        if shortcut_key and parent:
#            self.setup_shortcut(shortcut_key, parent)
#    
#    def setup_shortcut(self, shortcut_key, parent):
#        """Setup keyboard shortcut for this group"""
#        self.shortcut = QShortcut(QKeySequence(shortcut_key), parent)
#        self.shortcut.activated.connect(self.toggle_content)
#        
#    def toggle_content(self):
#        if self.expanded:
#            self.content_widget.hide()
#            button_text = self.toggle_button.text().replace("▼", "▶")
#            self.toggle_button.setText(button_text)
#            self.expanded = False
#        else:
#            self.content_widget.show()
#            button_text = self.toggle_button.text().replace("▶", "▼")
#            self.toggle_button.setText(button_text)
#            self.expanded = True
#    
#    def addWidget(self, widget):
#        self.content_layout.addWidget(widget)
#        
#    def set_expanded(self, expanded):
#        """Programmatically expand or collapse"""
#        if expanded != self.expanded:
#            self.toggle_content()

class CategoryFilter(QWidget):
    filterChanged = pyqtSignal(list)
    
    def __init__(self, categories):
        super().__init__()
        self.categories = categories
        self.checkboxes = {}
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Quick action buttons
        button_layout = QHBoxLayout()
        select_all_btn = QPushButton("All")
        select_all_btn.setMaximumWidth(50)
        select_all_btn.clicked.connect(self.select_all)
        
        clear_btn = QPushButton("None")
        clear_btn.setMaximumWidth(50)
        clear_btn.clicked.connect(self.clear_all)
        
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Category checkboxes
        for category in self.categories:
            checkbox = QCheckBox(category)
            checkbox.setChecked(True)  # Start with all selected
            checkbox.stateChanged.connect(self.on_selection_changed)
            self.checkboxes[category] = checkbox
            layout.addWidget(checkbox)
            
    def select_all(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)
            
    def clear_all(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
            
    def on_selection_changed(self):
        selected = [cat for cat, cb in self.checkboxes.items() if cb.isChecked()]
        self.filterChanged.emit(selected)
        
    def get_selected_categories(self):
        return [cat for cat, cb in self.checkboxes.items() if cb.isChecked()]

class TransactionFilterUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Filter - Recommended Approach")
        self.setGeometry(100, 100, 1200, 700)
        
        # Sample categories (typical for credit cards)
        self.categories = [
            "Groceries", "Restaurants", "Gas/Fuel", "Shopping", "Entertainment",
            "Bills/Utilities", "Healthcare", "Travel", "Education", "Other"
        ]
        
        # Sample transaction data
        self.all_transactions = self.generate_sample_data()
        self.filtered_transactions = self.all_transactions.copy()
        
        self.setup_ui()
        self.apply_filters()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        central_widget_layout = QHBoxLayout(central_widget)
        central_widget_layout.addWidget(splitter)
        
        # Left panel - Filters
        filter_panel = QWidget()
        filter_panel.setMaximumWidth(300)
        filter_panel.setMinimumWidth(250)
        filter_layout = QVBoxLayout(filter_panel)
        
        title_label = QLabel("Filters")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        filter_layout.addWidget(title_label)
        
        # Date Range Filter
        date_group = CollapsibleGroupBox("Date Range", "Ctrl+1", self)
        
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("From:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        self.date_from.dateChanged.connect(self.apply_filters)
        date_layout.addWidget(self.date_from)
        
        date_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.dateChanged.connect(self.apply_filters)
        date_layout.addWidget(self.date_to)
        
        date_group.content_layout.addLayout(date_layout)
        filter_layout.addWidget(date_group)
        
        # Amount Range Filter
        amount_group = CollapsibleGroupBox("Amount Range", "Ctrl+2", self)
        
        amount_layout = QVBoxLayout()
        amount_group.addWidget(QLabel("Min Amount:"))
        #amount_layout.addWidget(QLabel("Min Amount:"))
        self.amount_min = QLineEdit()
        self.amount_min.setPlaceholderText("0.00")
        self.amount_min.textChanged.connect(self.apply_filters)
        amount_group.addWidget(self.amount_min)
        #amount_layout.addWidget(self.amount_min)
        
        amount_group.addWidget(QLabel("Max Amount:"))
        #amount_layout.addWidget(QLabel("Max Amount:"))
        self.amount_max = QLineEdit()
        self.amount_max.setPlaceholderText("No limit")
        self.amount_max.textChanged.connect(self.apply_filters)
        amount_group.addWidget(self.amount_max)
        #amount_layout.addWidget(self.amount_max)
        
        #amount_group.content_layout.addLayout(amount_layout)
        #amount_group.addLayout(amount_layout)
        
        filter_layout.addWidget(amount_group)
        
        # Category Filter - The main focus
        category_group = CollapsibleGroupBox("Categories", "Ctrl+3", self)
        
        self.category_filter = CategoryFilter(self.categories)
        self.category_filter.filterChanged.connect(self.apply_filters)
        #category_group.content_layout.addWidget(self.category_filter)
        category_group.addWidget(self.category_filter)
        
        filter_layout.addWidget(category_group)
        
        # Store references to groups for global shortcuts only
        self.filter_groups = [date_group, amount_group, category_group]
        
        # Setup global shortcuts (these make sense at the main window level)
        self.setup_global_shortcuts()
        
        # Reset button
        reset_btn = QPushButton("Reset All Filters")
        reset_btn.clicked.connect(self.reset_filters)
        filter_layout.addWidget(reset_btn)
        
        filter_layout.addStretch()
        
        # Right panel - Results
        results_panel = QWidget()
        results_layout = QVBoxLayout(results_panel)
        
        # Results header
        self.results_label = QLabel()
        results_font = QFont()
        results_font.setBold(True)
        self.results_label.setFont(results_font)
        results_layout.addWidget(self.results_label)
        
        # Transaction table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Description", "Category", "Amount"])
        
        # Make table look nice
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        results_layout.addWidget(self.table)
        
        # Add panels to splitter
        splitter.addWidget(filter_panel)
        splitter.addWidget(results_panel)
        splitter.setSizes([300, 900])
        
    def setup_global_shortcuts(self):
        """Setup global shortcuts that affect multiple groups"""
        # Global shortcuts make sense at the main window level
        expand_all = QShortcut(QKeySequence("Ctrl+Shift+E"), self)
        expand_all.activated.connect(self.expand_all_filters)
        
        collapse_all = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        collapse_all.activated.connect(self.collapse_all_filters)
        
        # Reset filters shortcut
        reset_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        reset_shortcut.activated.connect(self.reset_filters)
        
        # Add help text
        self.setWindowTitle("Transaction Filter - Keyboard Shortcuts: Ctrl+1/2/3 (toggle sections), Ctrl+Shift+E/C (expand/collapse all), Ctrl+R (reset)")
    
    def expand_all_filters(self):
        """Expand all filter sections"""
        for group in self.filter_groups:
            group.set_expanded(True)
    
    def collapse_all_filters(self):
        """Collapse all filter sections"""
        for group in self.filter_groups:
            group.set_expanded(False)
        
    def generate_sample_data(self):
        transactions = []
        descriptions = {
            "Groceries": ["Walmart", "Target", "Kroger", "Whole Foods"],
            "Restaurants": ["McDonald's", "Chipotle", "Local Diner", "Pizza Place"],
            "Gas/Fuel": ["Shell", "BP", "Exxon", "Chevron"],
            "Shopping": ["Amazon", "Best Buy", "Macy's", "Home Depot"],
            "Entertainment": ["Netflix", "Movie Theater", "Concert", "Spotify"],
            "Bills/Utilities": ["Electric Bill", "Water Bill", "Internet", "Phone"],
            "Healthcare": ["Doctor Visit", "Pharmacy", "Dentist", "Insurance"],
            "Travel": ["Hotel", "Airline", "Uber", "Rental Car"],
            "Education": ["Tuition", "Books", "Online Course", "Supplies"],
            "Other": ["ATM Fee", "Bank Fee", "Misc Purchase", "Cash Back"]
        }
        
        for i in range(200):
            date = datetime.now() - timedelta(days=random.randint(1, 60))
            category = random.choice(self.categories)
            description = random.choice(descriptions[category])
            amount = round(random.uniform(5.0, 500.0), 2)
            
            transactions.append({
                'date': date,
                'description': description,
                'category': category,
                'amount': amount
            })
            
        return sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    def apply_filters(self):
        filtered = []
        
        # Get filter values
        date_from = self.date_from.date().toPyDate()
        date_to = self.date_to.date().toPyDate()
        selected_categories = self.category_filter.get_selected_categories()
        
        # Amount filters
        try:
            min_amount = float(self.amount_min.text()) if self.amount_min.text() else 0
        except ValueError:
            min_amount = 0
            
        try:
            max_amount = float(self.amount_max.text()) if self.amount_max.text() else float('inf')
        except ValueError:
            max_amount = float('inf')
        
        # Apply filters
        for transaction in self.all_transactions:
            # Date filter
            trans_date = transaction['date'].date()
            if not (date_from <= trans_date <= date_to):
                continue
                
            # Category filter
            if transaction['category'] not in selected_categories:
                continue
                
            # Amount filter
            if not (min_amount <= transaction['amount'] <= max_amount):
                continue
                
            filtered.append(transaction)
        
        self.filtered_transactions = filtered
        self.update_table()
        
    def update_table(self):
        self.table.setRowCount(len(self.filtered_transactions))
        
        for row, transaction in enumerate(self.filtered_transactions):
            self.table.setItem(row, 0, QTableWidgetItem(transaction['date'].strftime('%m/%d/%Y')))
            self.table.setItem(row, 1, QTableWidgetItem(transaction['description']))
            self.table.setItem(row, 2, QTableWidgetItem(transaction['category']))
            self.table.setItem(row, 3, QTableWidgetItem(f"${transaction['amount']:.2f}"))
        
        # Update results label
        total_amount = sum(t['amount'] for t in self.filtered_transactions)
        self.results_label.setText(
            f"Showing {len(self.filtered_transactions)} transactions "
            f"(Total: ${total_amount:.2f})"
        )
    
    def reset_filters(self):
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_to.setDate(QDate.currentDate())
        self.amount_min.clear()
        self.amount_max.clear()
        self.category_filter.select_all()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransactionFilterUI()
    window.show()
    sys.exit(app.exec_())
