from model import Importer, Categories
from view import CategorizeScreen, AddNewRuleScreen, ImportCompleteScreen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class CategorizeController:
    def __init__(self, main: "MainController", categorize_screen: CategorizeScreen, add_new_rule_screen: AddNewRuleScreen, import_complete_screen: ImportCompleteScreen, importer: Importer, categories: Categories):
        self.main = main
        self.categorize_screen = categorize_screen
        self.add_new_rule_screen = add_new_rule_screen
        self.import_complete_screen = import_complete_screen
        self.importer = importer
        self.categories = categories
        self.index = 0
        self.category = ''
        self.guessed_category = ''
        self.purpose = self.add_new_rule_screen.Purpose.NEW_RULE

        # button wiring
        self.categorize_screen.continue_clicked.connect(self.on_continue_clicked)
        self.categorize_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.categorize_screen.skip_clicked.connect(self.on_skip_clicked)
        self.categorize_screen.category_chosen.connect(self.on_category_chosen)
        self.add_new_rule_screen.continue_clicked.connect(self.on_add_new_continue_clicked)
        self.add_new_rule_screen.cancel_clicked.connect(self.on_add_new_cancel_clicked)
        self.import_complete_screen.cancel_clicked.connect(self.on_import_complete_cancel_clicked)
        self.import_complete_screen.continue_clicked.connect(self.on_import_complete_continue_clicked)

    def start(self):
        self.index = 0
        self.categorize_screen.update_category_buttons(self.categories)
        self.display_and_guess_current_transaction()

    def display_and_guess_current_transaction(self):
        self.categorize_screen.display_transaction(self.importer[self.index], self.index, len(self.importer))
        self.guess_category()

    def check_activate_continue_button(self):
        enable = bool(self.category in self.categories or self.category == 'New Category')
        self.categorize_screen.set_continue_button_enabled(enable)

    def set_category_and_advance(self):
        self.importer.set_category(self.index, self.category)
        self.index += 1
        if self.index < len(self.importer):
            self.display_and_guess_current_transaction()
        else:
            self.main.go_to_screen('import_complete')

    def guess_category(self):
        self.guessed_category = self.categories.guess_category(self.importer[self.index]['Location'])
        self.category = self.guessed_category
        self.categorize_screen.guess_category(self.guessed_category)
        self.check_activate_continue_button()

    def on_category_chosen(self, category: str):
        self.category = category
        self.check_activate_continue_button()

    def on_continue_clicked(self):
        """
        * handles new category and new category rules
        * sets the category in self.importer
        * advances to next transaction
        """
        if self.category == 'New Category':
            self.go_to_add_new_rule_screen(AddNewRuleScreen.Purpose.NEW_CATEGORY)
            return

        if self.category != self.guessed_category:
            self.go_to_add_new_rule_screen(AddNewRuleScreen.Purpose.NEW_RULE)
            return

        self.set_category_and_advance()

    def on_cancel_clicked(self):
        if self.index <= 0:
            self.reset()
            self.main.go_to_screen('import')
        else:
            self.index -= 1
            self.display_and_guess_current_transaction()

    def on_skip_clicked(self):
        self.importer.pop(self.index)
        if self.index < len(self.importer):
            self.display_and_guess_current_transaction()
        else:
            self.main.go_to_screen('import_complete')

    def on_add_new_continue_clicked(self, text: str):
        match self.purpose:
            case AddNewRuleScreen.Purpose.NEW_RULE:
                self.categories.add_new_category_rule(text, self.category)
            case AddNewRuleScreen.Purpose.NEW_CATEGORY:
                self.category = text
                self.categories.add_new_category(text)
                self.categorize_screen.update_category_buttons(self.categories)
            case _:
                print(f'Unexpected value "{self.purpose}" in CategorizeController.on_add_new_continue_clicked')
        self.return_to_categorize_screen()
        self.set_category_and_advance()

    def on_add_new_cancel_clicked(self):
        self.return_to_categorize_screen()
        match self.purpose:
            case AddNewRuleScreen.Purpose.NEW_RULE:
                self.set_category_and_advance()
            case AddNewRuleScreen.Purpose.NEW_CATEGORY:
                pass # just return to categorize screen
            case _:
                print(f'Unexpected value "{self.purpose}" in CategorizeController.on_add_new_cancel_clicked')

    def on_import_complete_continue_clicked(self):
        self.importer.insert_records_into_database()
        self.main.go_to_screen('home')
        self.main.reset_import_process()

    def on_import_complete_cancel_clicked(self):
        self.on_cancel_clicked()
        self.return_to_categorize_screen()

    def add_new_category_rule(self, keyword: str):
        self.categories.add_new_category_rule(keyword, self.category)
        self.add_new_rule_to_categorize_screen()

    def add_new_category(self, category: str):
        self.importer.add_new_category(category)

    def go_to_add_new_rule_screen(self, purpose):
        self.purpose = purpose
        self.add_new_rule_screen.set_purpose(purpose)
        self.add_new_rule_screen.display_transaction(self.importer[self.index], self.index, len(self.importer))
        self.main.go_to_screen('add_new_rule')

    def return_to_categorize_screen(self):
        self.main.go_to_screen('categorize')

    def reset(self):
        self.categorize_screen.reset()
        self.add_new_rule_screen.reset()
        self.import_complete_screen.reset()
        self.index = 0
        self.category = ''
        self.guessed_category = ''

