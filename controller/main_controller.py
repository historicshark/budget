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
            'edit_record': EditRecordScreen(),
        }
        self.screen_indexes = {}
        self.register_screens()

        self.controllers = {
            'import': ImportController(self, self.screens['import'], self.importer),
            'categorize': CategorizeController(self, self.screens['categorize'], self.screens['add_new_rule'], self.screens['import_complete'], self.importer, self.categories),
            'filter': FilterController(self, self.screens['filter'], self.db, self.categories),
            'expenses': ExpensesController(self, self.screens['expenses'], self.db),
            'list': ListController(self, self.screens['list'], self.db),
            'edit_record': EditRecordController(self, self.screens['edit_record'], self.db, self.categories),
        }

        # connections
        self.screens['home'].import_clicked.connect(lambda: self.go_to_screen('import'))
        self.screens['home'].expenses_clicked.connect(self.start_expenses)
        self.screens['home'].list_clicked.connect(self.start_list)

    def register_screens(self):
        for name, screen in self.screens.items():
            self.main_window.stack.addWidget(screen)
            self.screen_indexes[name] = self.main_window.stack.indexOf(screen)

            if hasattr(screen, 'home_clicked'):
                screen.home_clicked.connect(lambda: self.go_to_screen('home'))
    
    def debug(self):
        self.start_list()
        self.screens['filter'].date_filter.menu.setCurrentIndex(1)
        self.screens['filter'].amount_check_box.setChecked(False)
        self.screens['filter'].category_check_box.setChecked(False)
        self.controllers['filter'].on_continue_clicked()

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
        print('start expenses')
        self.go_to_screen('filter')
        self.controllers['filter'].disconnect_all()
        self.controllers['filter'].cancel_clicked.connect(lambda: self.go_to_screen('home'))
        self.controllers['filter'].continue_clicked.connect(self.set_records_and_go_to_expenses_screen)

    def start_list(self):
        print('start list')
        self.go_to_screen('filter')
        self.controllers['filter'].disconnect_all()
        self.controllers['filter'].cancel_clicked.connect(lambda: self.go_to_screen('home'))
        self.controllers['filter'].continue_clicked.connect(self.set_records_and_go_to_list_screen)

    def set_records_and_go_to_expenses_screen(self):
        self.controllers['expenses'].records = self.controllers['filter'].records
        self.go_to_screen('expenses')
        self.controllers['expenses'].update_views()

    def set_records_and_go_to_list_screen(self):
        self.controllers['list'].records = self.controllers['filter'].records
        self.go_to_screen('list')
        self.controllers['list'].sort_records_by_date()
        self.controllers['list'].update_table()

    def list_screen_to_edit_record_screen(self, records_to_edit: list[Record]):
        for record in records_to_edit:
            print(record)

    def update_records_in_list_controller_screen(self):
        """ after deleting records from the list, use the filters to get the
        updated records from the database """
        self.controllers['list'].records = self.db.select_filter(self.controllers['filter'].filter)
        self.controllers['list'].sort_records(self.screens['list'].drop_down.currentText())

    def print_records(self):
        records = self.controllers['filter'].records
        self.db.print_records(records)
