from PyQt5.QtCore import pyqtSignal, QObject

from model import Categories, Record
from view import AddNewCategoryScreen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class AddNewCategoryController(QObject):
    """ 
    - connect/disconnect continue and cancel in main controller
    - continue_clicked emits the new category
    """
    continue_clicked = pyqtSignal(str)
    cancel_clicked  = pyqtSignal()

    def __init__(self, main: 'MainController', add_new_category_screen: AddNewCategoryScreen, categories: Categories):
        super().__init__()
        self.main = main
        self.add_new_category_screen = add_new_category_screen
        self.categories = categories

        # wiring
        self.add_new_category_screen.continue_clicked.connect(self.on_continue_clicked)
        self.add_new_category_screen.cancel_clicked.connect(self.on_cancel_clicked)

    def display_record(self, record: Record):
        self.add_new_category_screen.display_record(record)
    
    def on_continue_clicked(self, new_category: str):
        self.categories.add_new_category(new_category)
        self.continue_clicked.emit(new_category)

    def on_cancel_clicked(self):
        self.cancel_clicked.emit()

    def disconnect_all(self):
        # disconnect() raises a TypeError if there are no connections but I don't care
        try:
            self.continue_clicked.disconnect()
        except TypeError:
            pass

        try:
            self.cancel_clicked.disconnect()
        except TypeError:
            pass

    def connect_continue_cancel(self, continue_connect, cancel_connect):
        self.disconnect_all()
        self.continue_clicked.connect(continue_connect)
        self.cancel_clicked.connect(cancel_connect)
