from model import *
from view import *
from controller import *

class MainController:
    def __init__(self):
        self.db = DatabaseManager('transactions')
        self.categories = Categories()
        self.importer = Importer(self.db, self.categories)

        self.main_window = MainWindow()
        self.screens = {
            'home': HomeScreen(),
            'import': ImportScreen(),
            'categorize': CategorizeScreen(),
            'add_new_rule': AddNewRuleScreen(),
            'import_complete': ImportCompleteScreen(),
            'filter': FilterScreen(),
            'plot': PlotScreen(),
        }
        self.screen_indexes = {}
        self.register_screens()

        self.controllers = {
            'import': ImportController(self, self.screens['import'], self.importer),
            'categorize': CategorizeController(self, self.screens['categorize'], self.screens['add_new_rule'], self.screens['import_complete'], self.importer),
            'filter': FilterController(self, self.screens['filter'], self.db, self.categories),
            'plot': PlotController(self, self.screens['plot'], self.db),
        }

        # connections
        self.screens['home'].import_clicked.connect(lambda: self.go_to_screen('import'))
        self.screens['home'].plot_clicked.connect(self.start_plot)

    def register_screens(self):
        for name, screen in self.screens.items():
            self.main_window.stack.addWidget(screen)
            self.screen_indexes[name] = self.main_window.stack.indexOf(screen)

            if hasattr(screen, 'home_clicked'):
                screen.home_clicked.connect(lambda: self.go_to_screen('home'))
    
    def debug(self):
        self.go_to_screen('home')

    def start(self):
        self.main_window.show()
        self.debug() #XXX debug

    def go_to_screen(self, name):
        if name in self.screens.keys():
            print(f'go to {name}')
            self.main_window.stack.setCurrentIndex(self.screen_indexes[name])
        else:
            print(f'screen {name} not implemented')

    def import_to_categorize_screen(self):
        self.go_to_screen('categorize')
        self.controllers['categorize'].start()
    
    def categorize_to_new_category_screen(self): #TODO
        self.go_to_screen('new_category')

    def reset_import_process(self):
        self.controllers['import'].reset()
        self.controllers['categorize'].reset()

    def start_plot(self):
        self.go_to_screen('filter')

        self.controllers['filter'].cancel_clicked.connect(lambda: self.go_to_screen('home'))
        self.controllers['filter'].continue_clicked.connect(self.set_records_and_go_to_plot_screen)

    def set_records_and_go_to_plot_screen(self):
        self.controllers['plot'].records = self.controllers['filter'].records
        self.go_to_screen('plot')
        self.controllers['plot'].plot()

    def print_records(self):
        records = self.controllers['filter'].records
        self.db.print_records(records)

