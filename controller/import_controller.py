from pathlib import Path

from model import Categories, Importer
from view import ImportScreen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class ImportController:
    def __init__(self, main: "MainController", screen: ImportScreen, importer: Importer):
        self.file = ''
        self.file_exists = False
        self.account = ''

        self.screen = screen
        self.importer = importer
        self.main = main

        # button wiring
        self.screen.account_clicked.connect(self.on_account_button_toggled)
        self.screen.file_chosen.connect(self.on_file_chosen)
        self.screen.continue_clicked.connect(self.on_continue_clicked)
        self.screen.cancel_clicked.connect(self.on_cancel_clicked)
    
    def on_file_chosen(self, file: str):
        self.file_exists = Path(file).exists()
        if self.file_exists:
            self.file = file
        self.check_activate_account_buttons()
        self.check_activate_continue_button()

    def on_account_button_toggled(self, account: str):
        self.account = account
        self.check_activate_continue_button()
        
    def check_activate_account_buttons(self):
        if self.file_exists and self.file.lower().endswith('.csv'):
            self.screen.set_account_buttons_visibility(True)
        else:
            self.screen.set_account_buttons_visibility(False)

    def check_activate_continue_button(self):
        enable = bool(self.file_exists and (self.file.lower().endswith(('.ofx','.qbo','.qfx')) or (self.account and self.file.lower().endswith('.csv'))))
        self.screen.set_continue_button_enabled(enable)

    def on_continue_clicked(self):
        self.importer.set_file(self.file)
        self.importer.import_file(self.account)
        self.main.import_to_categorize_screen()

    def on_cancel_clicked(self):
        self.reset()
        self.screen.home_clicked.emit()

    def reset(self):
        self.screen.reset()
        self.file = ''
        self.file_exists = False
        self.account = ''
        self.check_activate_continue_button()
        self.check_activate_account_buttons()
