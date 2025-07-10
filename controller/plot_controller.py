from PyQt5.QtCore import QObject

from view import PlotScreen
from model import DatabaseManager

from decimal import Decimal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class PlotController(QObject):
    def __init__(self, main: "MainController", plot_screen: PlotScreen, db: DatabaseManager):
        super().__init__()

        self.main = main
        self.plot_screen = plot_screen
        self.db = db

        self.records = []

        self.plot_screen.new_search_clicked.connect(self.on_new_search_clicked)

    def plot(self):
        self.db.print_records(self.records) #XXX debug

        # get totals by category
        totals = {}
        for record in self.records:
            amount = Decimal(record['Amount'])
            category = record['Category']
            if category not in totals.keys():
                totals[category] = 0
            totals[category] += amount

        # separate into income and expenses
        income = {category: amount for category, amount in totals.items() if amount > 0}
        expenses = {category: -amount for category, amount in totals.items() if amount <= 0}

        self.plot_screen.plot_expenses(expenses.keys(), expenses.values())
        self.plot_screen.plot_income(income.keys(), income.values())

    def on_new_search_clicked(self):
        self.main.go_to_screen('filter')
