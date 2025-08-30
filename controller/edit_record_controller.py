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

    
