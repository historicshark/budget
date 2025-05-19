from pathlib import Path

from model.database import DatabaseManager
from model.import_categorize import Importer
from view.import_screen import ImportScreen

class ImportController:
    def __init__(self, screen: ImportScreen, main, importer: Importer):
        self.file = ''
        self.file_exists = False
        self.account = ''
    
    def check_activate_account_buttons(self):
        if self.file_exists and self.file.lower().endswith('.csv'):
            self.set_account_buttons_visibility(True)
        else:
            self.set_account_buttons_visibility(False)
    