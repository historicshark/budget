from PyQt5.QtCore import pyqtSignal

from model import DatabaseManager

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class FilterController:
    retrieve_records = pyqtSignal(list)

    def __init__(self, main: "MainController", filter_screen: FilterScreen, db: DatabaseManager):
        self.main = main
        self.filter_screen = filter_screen
        self.db = db

        self.filter = dict('Date': None, 'Amount': None, 'Category': None)
        self.records: list[dict[str, str]] = []

        # button wiring
        self.filter_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.filter_screen.continue_clicked.connect(self.on_continue_clicked)
        self.filter_screen.filter_changed.connect(self.on_filter_changed)

    def start(self):
        self.

    def on_filter_changed(self, filters):
        """
        filters: dict['Date': (datetime.date)*2 | None,
                      'Amount': (float)*2 | None,
                      'Category': list[str] | None
                      ]
        """
        self.filter = filters

    def on_continue_clicked(self):
        self.retrieve_records.emit(self.records)

    def on_cancel_clicked(self):
        self.filter_screen.reset()
        self.main.go_to_screen('home')

