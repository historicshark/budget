from PyQt5.QtCore import QObject

from view import ExpensesScreen
from model import DatabaseManager, Categories

import datetime
from decimal import Decimal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class ExpensesController(QObject):
    def __init__(self, main: "MainController", expenses_screen: ExpensesScreen, db: DatabaseManager):
        super().__init__()

        self.main = main
        self.expenses_screen = expenses_screen
        self.db = db

        # list of records to be plotted. set this from main controller
        self.records = []

        self.expenses_screen.new_search_clicked.connect(self.on_new_search_clicked)

    def update_views(self):
        self.db.print_records(self.records) #XXX debug

        # sort records by category
        totals = {}
        dates = {}
        locations = {}
        amounts = {}
        for record in self.records:
            amount = Decimal(record['Amount'])
            category = record['Category']
            if category not in totals.keys():
                totals[category] = 0
                dates[category] = []
                locations[category] = []
                amounts[category] = []
            totals[category] += amount
            dates[category].append(record['Date'])
            locations[category].append(record['Location'])
            amounts[category].append(record['Amount'])

        # sort lists by date
        for category in dates.keys():
            sorted_indexes = [p[0] for p in sorted(enumerate(dates[category]), key=lambda x: datetime.date.fromisoformat(x[1]))]
            dates[category] = [dates[category][i] for i in sorted_indexes]
            locations[category] = [locations[category][i] for i in sorted_indexes]
            amounts[category] = [amounts[category][i] for i in sorted_indexes]

        # separate into income and expenses
        income = {category: amount for category, amount in totals.items() if amount > 0}
        expenses = {category: -amount for category, amount in totals.items() if amount <= 0}

        self.expenses_screen.update_plot_view(expenses.keys(), expenses.values())
        self.expenses_screen.update_list_view(expenses.keys(), dates, locations, amounts, expenses)

    def on_new_search_clicked(self):
        self.main.go_to_screen('filter')
