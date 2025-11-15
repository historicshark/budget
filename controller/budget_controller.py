from PyQt5.QtCore import QObject

from view import BudgetScreen
from model import Categories, DatabaseManager

import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class BudgetController(QObject):
    def __init__(self, main: "MainController", budget_screen: BudgetScreen, categories: Categories, db: DatabaseManager):
        super().__init__()

        self.main = main
        self.budget_screen = budget_screen
        self.categories = categories
        self.db = db

        # Set date range to last month
        self.date_range = [
            (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1),
            datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        ]

        # wiring
        self.budget_screen.continue_clicked.connect(self.on_continue_clicked)
        self.budget_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.budget_screen.date_range_changed.connect(self.on_date_range_changed)
        self.categories.categories_updated.connect(self.update_screen)
        self.categories.amounts_updated.connect(self.update_screen)

    def update_screen(self):
        categories_values = self.db.totals_by_category(date=self.date_range)
        # make sure the result isn't empty
        if categories_values:
            categories_budget, values_budget = [list(x) for x in zip(*categories_values)]
        else:
            categories_budget = []
            values_budget = []

        # Doing this because the order of self.categories, self.categories.amounts, and values need to align
        values = []
        for category, category_type in zip(self.categories, self.categories.types):
            multiplier = self.categories.available_types[category_type]
            if category in categories_budget:
                values.append(multiplier * values_budget[categories_budget.index(category)])
            # for categories that have no spending in this time period, set the value to zero
            else:
                values.append(0)

        self.budget_screen.update_budget(self.categories, self.categories.amounts, values, self.categories.types)

    def on_date_range_changed(self, date_range: list):
        self.date_range = date_range
        self.update_screen()

    def on_continue_clicked(self):
        self.main.go_to_screen('home')

    def on_cancel_clicked(self):
        self.main.go_to_screen('home')
