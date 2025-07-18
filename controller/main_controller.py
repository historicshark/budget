from model import *
from view import *
from controller import *

class MainController:
    def __init__(self):
        self.db = DatabaseManager('transactions')
        self.categories = Categories()
        self.importer = Importer(self.db)

        self.main_window = MainWindow()
        self.screens = {
            'home': HomeScreen(),
            'import': ImportScreen(),
            'categorize': CategorizeScreen(),
            'add_new_rule': AddNewRuleScreen(),
            'import_complete': ImportCompleteScreen(),
            'filter': FilterScreen(),
            'expenses': ExpensesScreen(),
            'list': ListScreen(),
        }
        self.screen_indexes = {}
        self.register_screens()

        self.controllers = {
            'import': ImportController(self, self.screens['import'], self.importer),
            'categorize': CategorizeController(self, self.screens['categorize'], self.screens['add_new_rule'], self.screens['import_complete'], self.importer, self.categories),
            'filter': FilterController(self, self.screens['filter'], self.db, self.categories),
            'expenses': ExpensesController(self, self.screens['expenses'], self.db),
        }

        # connections
        self.screens['home'].import_clicked.connect(lambda: self.go_to_screen('import'))
        self.screens['home'].expenses_clicked.connect(self.start_expenses)
        self.screens['home'].list_clicked.connect(lambda: self.go_to_screen('list'))

    def register_screens(self):
        for name, screen in self.screens.items():
            self.main_window.stack.addWidget(screen)
            self.screen_indexes[name] = self.main_window.stack.indexOf(screen)

            if hasattr(screen, 'home_clicked'):
                screen.home_clicked.connect(lambda: self.go_to_screen('home'))
    
    def debug(self):
        self.go_to_screen('list')
        records = self.db.select()
        self.screens['list'].update_table(records)

    def start(self):
        self.main_window.show()
        self.go_to_screen('home')
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

    def reset_import_process(self):
        self.controllers['import'].reset()
        self.controllers['categorize'].reset()

    def start_expenses(self):
        self.go_to_screen('filter')
        self.controllers['filter'].cancel_clicked.connect(lambda: self.go_to_screen('home'))
        self.controllers['filter'].continue_clicked.connect(self.set_records_and_go_to_expenses_screen)
        self.controllers['filter'].start()

    def start_list(self):
        self.go_to_screen('filter')
        self.controllers['filter'].cancel_clicked.connect(lambda: self.go_to_screen('home'))
        self.controllers['filter'].continue_clicked.connect(lambda: print('not implemented')) #TODO
        self.go_to_screen('list')
        self.screens['list'].update_table(self.db.select())

    def set_records_and_go_to_expenses_screen(self):
        self.controllers['expenses'].records = self.controllers['filter'].records
        self.go_to_screen('expenses')
        self.controllers['expenses'].update_views()

    def print_records(self):
        records = self.controllers['filter'].records
        self.db.print_records(records)

