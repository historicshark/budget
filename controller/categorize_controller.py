from model.import_categorize import Importer
from model.database import DatabaseManager
from view.categorize_screen import CategorizeScreen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class CategorizeController:
    def __init__(self, main: "MainController", screen: CategorizeScreen, importer: Importer):
        self.main = main
        self.screen = screen
        self.importer = importer
        self.index = 0
        self.category = ''

        # button wiring
        self.screen.continue_clicked.connect(self.on_continue_clicked)
        self.screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.screen.skip_clicked.connect(self.on_skip_clicked)
        # self.screen.category_chosen.connect()
    
    def start(self):
        self.display_current_transaction()


    def display_current_transaction(self):
        self.screen.display_transaction(self.importer[self.index], self.index, len(self.importer))

    def check_activate_continue_button(self):
        enable = bool(self.category in self.importer.categories or self.category == 'New Category')
        self.screen.set_continue_button_enabled(enable)
    
    def advance(self):
        self.index += 1
        if self.index < len(self.importer):
            self.display_current_transaction()
        else:
            self.main.go_to_screen('home')
            self.reset()

    def on_continue_clicked(self):
        if self.category == 'New Category':
            self.main.categorize_to_new_category_screen() #TODO
        else:
            self.importer.set_category(self.index, self.category)
            self.index += 1
            self.advance()
    
    def on_cancel_clicked(self):
        if self.index <= 0:
            self.reset()
            self.screen.home_clicked.emit()
        else:
            self.index -= 1
            self.display_current_transaction()
    
    def on_skip_clicked(self):
        self.importer.pop(self.index)
        if self.index < len(self.importer):
            self.display_current_transaction()
        else:
            self.main.go_to_screen('home')
            self.reset()
        
    def reset(self):
        self.index = 0
        self.category = ''