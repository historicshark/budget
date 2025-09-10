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
        self.list_screen.edit_clicked.connect(self.on_edit_clicked)
        self.list_screen.delete_clicked.connect(self.on_delete_clicked)

    def update_table(self):
        #self.db.print_records(self.records) #XXX debug
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

    def on_edit_clicked(self, indices_selected):
        records_to_edit = [self.records[i] for i in indices_selected]
        if len(records_to_edit) > 0:
            self.main.list_screen_to_edit_record_screen(records_to_edit)

    def on_delete_clicked(self, indices_selected):
        if len(indices_selected) > 0:
            for i in indices_selected:
                record = self.records[i]
                self.db.delete(date=record.date_str(), location=record.location, category=record.category, amount=record.amount_str())
            self.main.update_records_in_list_controller_screen()
