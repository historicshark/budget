from model.database import DatabaseManager
from model.import_categorize import Importer
from view.main_window import MainWindow
from view.home_screen import HomeScreen
from view.import_screen import ImportScreen
from controller.import_controller import ImportController

class MainController:
    def __init__(self):
        self.db = DatabaseManager('transactions')
        self.importer = Importer(self.db)

        # screens
        self.main_window = MainWindow()
        self.screens = {
            'home': HomeScreen(),
            'import': ImportScreen(),
        }
        self.screen_indexes = {}
        self.go_to = {}
        self.register_screens()

        self.controllers = {
            'import': ImportController(self, self.screens['import'], self.importer),
        }

        # home screen
        self.screens['home'].import_clicked.connect(self.go_to['import'])
    
    def register_screens(self):
        for name, screen in self.screens.items():
            self.main_window.stack.addWidget(screen)
            self.screen_indexes[name] = self.main_window.stack.indexOf(screen)
            self.go_to[name] = lambda: self.go_to_screen(name)

            if hasattr(screen, 'home_clicked'):
                screen.home_clicked.connect(lambda: self.go_to_screen('home'))
    
    def start(self):
        self.main_window.show()

    def go_to_screen(self, name):
        if name in self.screens.keys():
            self.main_window.stack.setCurrentIndex(self.screen_indexes[name])
        else:
            print(f'screen {name} not implemented')
