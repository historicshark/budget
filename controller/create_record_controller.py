from PyQt5.QtCore import QObject

from view import CreateRecordScreen
from model import DatabaseManager, Categories, Record

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class CreateRecordController(QObject):
    def __init__(self, main: 'MainController', create_record_screen: CreateRecordScreen, db: DatabaseManager, categories: Categories):
        super().__init__()

        self.main = main
        self.create_record_screen = create_record_screen
        self.db = db
        self.categories = categories

        self.update_category_options()

        self.create_record_screen.continue_clicked.connect(self.create_record)
        self.create_record_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.create_record_screen.new_category_clicked.connect(self.on_new_category_selected)

    def update_category_options(self):
        self.create_record_screen.update_category_options(self.categories)

    def on_new_category_selected(self):
        print('todo go to new category screen')

    def display_record(self, record: Record):
        self.edit_record_screen.display_record(record)

    def create_record(self, record: Record):
        self.db.insert_record(record)

    def on_cancel_clicked(self):
        self.main.go_to_screen('home')
