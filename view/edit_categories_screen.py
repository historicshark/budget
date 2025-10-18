from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QLineEdit,
    QApplication,
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from view import BaseScreen, colors
from view.widgets import ComboBoxFix

class EditCategoriesScreen(BaseScreen):
    home_clicked = pyqtSignal()
    continue_clicked = pyqtSignal(list) # list of changes (old, new)
    cancel_clicked = pyqtSignal()
    delete_clicked = pyqtSignal(list) # list of categories to delete

    def __init__(self):
        super().__init__()
        self.categories: list[str] = []
        self.old_types: list[str] = []
        self.check_boxes: list[QCheckBox] = []
        self.line_edits: list[QLineEdit] = []
        self.combo_boxes: list[ComboBoxFix] = []
        self.indices_selected: list[int] = []

        self.timer = QTimer()
        self.timer.setSingleShot(True)

        self.initUI()

    def initUI(self):
        self.add_title(self.content_layout, 'Edit Categories', self.home_clicked.emit, 20)

        # Scroll area with a grid layout for check boxes and categories
        list_widget = QWidget()
        self.list_layout = QGridLayout()
        list_widget.setLayout(self.list_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(list_widget)
        #self.scroll_area.verticalScrollBar().valueChanged.connect(self.print_scroll_bar) #XXX debug
        self.content_layout.addWidget(self.scroll_area)

        add_button = QPushButton('add new')
        add_button.clicked.connect(self.on_add_clicked)
        add_button.setFixedSize(150, 50)

        del_button = QPushButton('delete\nselected')
        del_button.clicked.connect(self.on_delete_clicked)
        del_button.setFixedSize(150, 50)
        del_button.setStyleSheet('font-size: 16px;')

        button_layout = self.add_continue_cancel_buttons(self.content_layout, self.on_continue_clicked, self.cancel_clicked.emit)
        button_layout.insertWidget(0, add_button)
        button_layout.insertSpacing(1, 20)
        button_layout.insertWidget(2, del_button)
        button_layout.insertStretch(3, 10)

        keys_functions = [
            ('<return>', 'continue'),
            ('<esc>', 'cancel'),
        ]
        self.add_footer(self.base_layout, keys_functions)

    def update_category_options(self, categories: list[str], types: list[str], available_types: list[str]):
        self.categories.clear()
        self.old_types.clear()
        self.check_boxes.clear()
        self.line_edits.clear()
        self.combo_boxes.clear()
        self.clear_layout(self.list_layout)

        self.list_layout.addWidget(QLabel('Category'), 0, 1)
        self.list_layout.addWidget(QLabel('Type'), 0, 2)

        for row, (category, category_type) in enumerate(zip(categories, types)):
            row += 1
            check_box = QCheckBox()
            line_edit = QLineEdit(category)
            line_edit.setStyleSheet('font-size: 15px;')
            combo_box = ComboBoxFix()
            combo_box.setFixedWidth(100)
            combo_box.view().setMinimumWidth(106)
            combo_box.addItems(available_types)
            combo_box.setCurrentText(category_type)
            self.list_layout.addWidget(check_box, row, 0)
            self.list_layout.addWidget(line_edit, row, 1)
            self.list_layout.addWidget(combo_box, row, 2)
            self.categories.append(category)
            self.old_types.append(category_type)
            self.check_boxes.append(check_box)
            self.line_edits.append(line_edit)
            self.combo_boxes.append(combo_box)

        n_rows = len(categories)
        self.list_layout.setColumnStretch(n_rows + 1, 3)
        self.list_layout.setRowStretch(n_rows + 1, 3)
        self.get_selected_indices()

    def scroll_to_bottom(self):
        vertical_scroll_bar = self.scroll_area.verticalScrollBar()
        vertical_scroll_bar.setValue(vertical_scroll_bar.maximum())

    def get_selected_indices(self) -> list[int]:
        self.indices_selected.clear()
        for row, check_box in enumerate(self.check_boxes):
            if check_box.isChecked():
                self.indices_selected.append(row)
        return self.indices_selected

    def get_selected_categories(self) -> list[str]:
        selected_categories = []
        for category, check_box in zip(self.categories, self.check_boxes):
            if check_box.isChecked():
                selected_categories.append(category)
        return selected_categories
    
    def get_category_changes(self) -> list[tuple[str, str, str, str]]:
        """ 
        returns all rows as a list of tuples of (old, new, old_type, new_type) categories.
        'New Category' is on the left
        """
        category_changes = []
        for category, line_edit, old_type, combo_box in zip(self.categories, self.line_edits, self.old_types, self.combo_boxes):
            category_changes.append((category, line_edit.text(), old_type, combo_box.currentText()))
        return category_changes

    def on_add_clicked(self):
        check_box = QCheckBox()
        line_edit = QLineEdit('New Category')
        line_edit.setStyleSheet('font-size: 15px;')
        available_types = [self.combo_boxes[-1].itemText(i) for i in range(self.combo_boxes[-1].count())]
        combo_box = ComboBoxFix()
        combo_box.setFixedWidth(100)
        combo_box.view().setMinimumWidth(106)
        combo_box.addItems(available_types)

        n_rows = len(self.categories)
        self.list_layout.addWidget(check_box, n_rows + 1, 0)
        self.list_layout.addWidget(line_edit, n_rows + 1, 1)
        self.list_layout.addWidget(combo_box, n_rows + 1, 2)

        self.categories.append('New Category')
        self.old_types.append(combo_box.currentText())
        self.check_boxes.append(check_box)
        self.line_edits.append(line_edit)
        self.combo_boxes.append(combo_box)

        # force scroll bar to update
        self.scroll_area.widget().updateGeometry()
        self.scroll_area.updateGeometry()
        QApplication.processEvents()

        self.scroll_to_bottom()

    def on_delete_clicked(self):
        if len(self.get_selected_indices()) > 0:
            # First clear the 'New Category' entries because they aren't in the database
            # or used by any records
            new_category_rows = [row for row in self.indices_selected if self.categories[row] == 'New Category']
            for row in reversed(new_category_rows):
                self.categories.pop(row)
                self.old_types.pop(row)
                check_box = self.check_boxes.pop(row)
                line_edit = self.line_edits.pop(row)
                combo_box = self.combo_boxes.pop(row)
                self.list_layout.removeWidget(check_box)
                self.list_layout.removeWidget(line_edit)
                self.list_layout.removeWidget(combo_box)
                check_box.deleteLater()
                line_edit.deleteLater()
                combo_box.deleteLater()

            self.delete_clicked.emit(self.get_selected_categories())

    def on_continue_clicked(self):
        self.continue_clicked.emit(self.get_category_changes())

    def print_scroll_bar(self, value): #XXX debug
        bar = self.scroll_area.verticalScrollBar()
        print(bar.minimum(), value, bar.maximum())
