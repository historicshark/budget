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
        self.is_purpose_new_rule = True

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

    def guess_category(self):
        self.guessed_category = self.categories.guess_category(self.importer[self.index].location)
        self.category = self.guessed_category
        self.categorize_screen.guess_category(self.guessed_category)
        self.check_activate_continue_button()

    def check_activate_continue_button(self):
        enable = bool(self.category in self.categories or self.category == 'New Category')
        self.categorize_screen.set_continue_button_enabled(enable)

    def advance(self):
        self.index += 1
        if self.index < len(self.importer):
            self.display_and_guess_current_transaction()
        else:
            self.main.go_to_screen('import_complete')

    def set_category_and_advance(self):
        self.importer.set_category(self.index, self.category)
        self.advance()

    def on_category_chosen(self, category: str):
        self.category = category
        self.check_activate_continue_button()

    def on_continue_clicked(self):
        if self.category == 'New Category':
            self.go_to_add_new_category_screen()
            return

        elif self.category != self.guessed_category:
            self.go_to_add_new_rule_screen()
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
        self.importer.skip_record(self.index)
        self.advance()

    def on_add_new_continue_clicked(self, text: str):
        if self.is_purpose_new_rule:
            self.categories.add_new_category_rule(text, self.category)
        else:
            self.category = text
            self.categories.add_new_category(text)
            self.categorize_screen.update_category_buttons(self.categories)
        self.return_to_categorize_screen()
        self.set_category_and_advance()

    def on_add_new_cancel_clicked(self):
        self.return_to_categorize_screen()
        if self.is_purpose_new_rule:
            self.set_category_and_advance()
        else:
            pass # just return to categorize screen

    def on_import_complete_continue_clicked(self):
        self.importer.insert_records_into_database()
        self.main.go_to_screen('home')
        self.main.reset_import_process()

    def on_import_complete_cancel_clicked(self):
        self.on_cancel_clicked()
        self.return_to_categorize_screen()

    def go_to_add_new_rule_screen(self):
        self.is_purpose_new_rule = True
        self.add_new_rule_screen.set_text_new_rule()
        self.add_new_rule_screen.display_transaction(self.importer[self.index], self.index, len(self.importer))
        self.main.go_to_screen('add_new_rule')

    def go_to_add_new_category_screen(self):
        self.is_purpose_new_rule = False
        self.add_new_rule_screen.set_text_new_category()
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
