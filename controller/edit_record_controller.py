from PyQt5.QtCore import QObject

from view import EditRecordScreen
from model import DatabaseManager, Categories, Record

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class EditRecordController(QObject):
    def __init__(self, main: 'MainController', edit_record_screen: EditRecordScreen, db: DatabaseManager, categories: Categories):
        super().__init__()

        self.main = main
        self.edit_record_screen = edit_record_screen
        self.db = db
        self.categories = categories

        self.records_to_edit: list[Record] = []
        self.records_edited: list[Record] = []
        self.index = 0

        self.update_category_options()

        # wiring
        self.edit_record_screen.continue_clicked.connect(self.advance)
        self.edit_record_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.edit_record_screen.new_category_clicked.connect(self.on_new_category_selected)
        self.categories.categories_updated.connect(self.update_category_options)

    def update_category_options(self):
        self.edit_record_screen.update_category_options(self.categories)

    def on_new_category_selected(self):
        self.main.go_to_add_new_category_screen(self.records_to_edit[self.index])

    def on_new_category_added(self, new_category):
        self.edit_record_screen.set_selected_category(new_category)

    def display_record(self):
        assert len(self.records_to_edit) > 0
        record = self.records_to_edit[self.index]
        self.edit_record_screen.display_record(record)

    def advance(self, new_record: Record):
        self.records_edited.append(new_record)
        self.index += 1

        if self.index < len(self.records_to_edit):
            self.display_record()
        else:
            assert len(self.records_to_edit) == len(self.records_edited)
            for old_record, new_record in zip(self.records_to_edit, self.records_edited):
                self.db.update_record(old_record, new_record)
            self.reset()
            self.main.update_records_in_list_controller_screen()
            self.main.go_to_screen('list')

    def on_cancel_clicked(self):
        self.reset()
        self.main.go_to_screen('list')

    def reset(self):
        self.records_to_edit = []
        self.records_edited = []
        self.index = 0
