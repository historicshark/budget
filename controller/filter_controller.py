from PyQt5.QtCore import pyqtSignal, QObject

from model import DatabaseManager, Categories, Record
from view import FilterScreen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class FilterController(QObject):
    """
    continue and cancel clicked need to be connected in the main controller because
    this screen can be reused in multiple places
    """
    cancel_clicked = pyqtSignal()
    continue_clicked = pyqtSignal()

    def __init__(self, main: "MainController", filter_screen: FilterScreen, db: DatabaseManager, categories: Categories):
        super().__init__()
        self.main = main
        self.filter_screen = filter_screen
        self.db = db
        self.categories = categories

        self.filter = {'Date': None, 'Amount': None, 'Category': None}
        self.records: list[Record] = []

        # wiring
        self.filter_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.filter_screen.continue_clicked.connect(self.on_continue_clicked)
        self.filter_screen.filter_changed.connect(self.on_filter_changed)
        self.categories.categories_updated.connect(self.update_category_options)

        self.update_category_options()

    def update_category_options(self):
        self.filter_screen.update_category_options(self.categories)

    def on_filter_changed(self, filters):
        """
        filters: dict['Date': (datetime.date)*2 | None,
                      'Amount': (float)*2 | None,
                      'Category': list[str] | None
                      ]
        """
        self.filter = filters

    def on_continue_clicked(self):
        self.records = self.db.select_filter(self.filter)
        self.continue_clicked.emit()

    def on_cancel_clicked(self):
        self.filter_screen.reset()
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

    def reset(self):
        self.filter_screen.reset()
