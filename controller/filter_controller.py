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

        # button wiring
        self.filter_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.filter_screen.continue_clicked.connect(self.on_continue_clicked)
        self.filter_screen.filter_changed.connect(self.on_filter_changed)

        self.filter_screen.update_category_buttons(self.categories)

    def start(self):
        pass

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
        """ Try disconnecting all slots. if they aren't connected, disconnect() gives an error,
        so use try/except to ignore the error
        """
        try:
            self.continue_clicked.disconnect()
        except:
            pass

        try:
            self.cancel_clicked.disconnect()
        except:
            pass

    def reset(self):
        self.filter_screen.reset()
