from model.database import DatabaseManager
from model.import_categorize import Importer
from view.main_window import MainWindow
from view.home_screen import HomeScreen
from view.import_screen import ImportScreen
from view.categorize_screen import CategorizeScreen
from controller.import_controller import ImportController
from controller.categorize_controller import CategorizeController

class MainController:
    def __init__(self):
        self.db = DatabaseManager('transactions')
        self.importer = Importer(self.db)

        self.main_window = MainWindow()
        self.screens = {
            'home': HomeScreen(),
            'import': ImportScreen(),
            'categorize': CategorizeScreen(),
        }
        self.screen_indexes = {}
        self.register_screens()

        self.controllers = {
            'import': ImportController(self, self.screens['import'], self.importer),
            'categorize': CategorizeController(self, self.screens['categorize'], self.importer),
        }

        # connections
        self.screens['home'].import_clicked.connect(lambda: self.go_to_screen('import'))
    
    def register_screens(self):
        for name, screen in self.screens.items():
            self.main_window.stack.addWidget(screen)
            self.screen_indexes[name] = self.main_window.stack.indexOf(screen)

            if hasattr(screen, 'home_clicked'):
                screen.home_clicked.connect(lambda: self.go_to_screen('home'))
    
    def start(self):
        self.main_window.show()

    def go_to_screen(self, name):
        if name in self.screens.keys():
            print(f'go to {name}')
            self.main_window.stack.setCurrentIndex(self.screen_indexes[name])
        else:
            print(f'screen {name} not implemented')

    def import_to_categorize_screen(self):
        self.go_to_screen('categorize')
        self.controllers['categorize'].display_current_transaction()
    
    def categorize_to_new_category_screen(self): #TODO
        self.go_to_screen('new_category')
