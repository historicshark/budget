from PyQt5.QtCore import QObject

from view import ListScreen
from model import DatabaseManager, Record

import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class ListController(QObject):
    def __init__(self, main: 'MainController', list_screen: ListScreen, db: DatabaseManager):
        super().__init__()

        self.main = main
        self.list_screen = list_screen
        self.db = db

        # list of records to be listed. set this from main controller
        self.records = []

        self.list_screen.new_search_clicked.connect(self.on_new_search_clicked)
        self.list_screen.sort_by_changed.connect(self.sort_records)

    def update_table(self):
        self.db.print_records(self.records)
        self.list_screen.update_table(self.records)

    def sort_records(self, sort_by: str):
        match sort_by.lower():
            case 'date':
                self.sort_records_by_date()
            case 'location':
                self.sort_records_by_location()
            case 'category':
                self.sort_records_by_category()
            case 'amount':
                self.sort_records_by_amount()
        self.update_table()

    def sort_records_by_date(self):
        self.records.sort(key=lambda record: record.date)

    def sort_records_by_location(self):
        self.records.sort(key=lambda record: record.location.lower())

    def sort_records_by_category(self):
        self.records.sort(key=lambda record: record.category)

    def sort_records_by_amount(self):
        self.records.sort(key=lambda record: record.amount)

    def on_new_search_clicked(self):
        self.main.go_to_screen('filter')
