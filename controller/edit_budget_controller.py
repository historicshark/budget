from PyQt5.QtCore import QObject

from view import EditBudgetScreen
from model import Categories

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class EditBudgetController(QObject):
    def __init__(self, main: 'MainController', edit_budget_screen: EditBudgetScreen, categories: Categories):
        super().__init__()

        self.main = main
        self.edit_budget_screen = edit_budget_screen
        self.categories = categories
        self.tmp_amounts = self.categories.amounts.copy()

        # wiring
        self.edit_budget_screen.continue_clicked.connect(self.on_continue_clicked)
        self.edit_budget_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.edit_budget_screen.amounts_changed.connect(self.on_amounts_changed)

        self.categories.categories_updated.connect(self.update_screen)
        self.categories.amounts_updated.connect(self.update_screen)

    def on_amounts_changed(self, amounts: list[float]):
        self.tmp_amounts = amounts
        self.update_summary_table()

    def update_category_options(self):
        self.edit_budget_screen.update_category_options(self.categories.categories, self.categories.amounts)

    def update_summary_table(self):
        """ update the table with values stored in self.tmp_amounts """
        amounts = dict.fromkeys(self.categories.available_types.keys(), 0.0)
        amounts['net'] = 0.0
        for t, a in zip(self.categories.types, self.tmp_amounts):
            amounts['net'] += self.categories.available_types[t] * a
            amounts[t] += a

        self.edit_budget_screen.update_summary_table(list(amounts.keys()),
                                                     list(amounts.values()))

    def update_screen(self):
        self.update_category_options()
        self.update_summary_table()

    def on_continue_clicked(self):
        self.categories.update_amounts(self.tmp_amounts)

    def on_cancel_clicked(self):
        self.main.go_to_screen('home')
        self.update_screen()
